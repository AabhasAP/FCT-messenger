class WebSocketService {
    private ws: WebSocket | null = null;
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;
    private reconnectDelay = 1000;
    private listeners: Map<string, Set<(data: any) => void>> = new Map();
    private workspaceId: string | null = null;

    connect(workspaceId: string, token: string) {
        this.workspaceId = workspaceId;
        const wsUrl = `${import.meta.env.VITE_WS_URL || 'ws://localhost:8000'}/ws/${workspaceId}?token=${token}`;

        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
            console.log('✓ WebSocket connected');
            this.reconnectAttempts = 0;
            this.startHeartbeat();
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            } catch (error) {
                console.error('Failed to parse WebSocket message:', error);
            }
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            this.stopHeartbeat();
            this.attemptReconnect();
        };
    }

    private handleMessage(data: any) {
        const { type } = data;
        const listeners = this.listeners.get(type);
        if (listeners) {
            listeners.forEach((callback) => callback(data));
        }

        // Also trigger wildcard listeners
        const wildcardListeners = this.listeners.get('*');
        if (wildcardListeners) {
            wildcardListeners.forEach((callback) => callback(data));
        }
    }

    on(eventType: string, callback: (data: any) => void) {
        if (!this.listeners.has(eventType)) {
            this.listeners.set(eventType, new Set());
        }
        this.listeners.get(eventType)!.add(callback);

        // Return unsubscribe function
        return () => {
            const listeners = this.listeners.get(eventType);
            if (listeners) {
                listeners.delete(callback);
            }
        };
    }

    off(eventType: string, callback: (data: any) => void) {
        const listeners = this.listeners.get(eventType);
        if (listeners) {
            listeners.delete(callback);
        }
    }

    send(data: any) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        } else {
            console.warn('WebSocket not connected');
        }
    }

    sendTyping(channelId: string, isTyping: boolean) {
        this.send({
            type: 'typing',
            channel_id: channelId,
            is_typing: isTyping,
        });
    }

    private heartbeatInterval: number | null = null;

    private startHeartbeat() {
        this.heartbeatInterval = window.setInterval(() => {
            this.send({ type: 'ping' });
        }, 30000); // 30 seconds
    }

    private stopHeartbeat() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
    }

    private attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts && this.workspaceId) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

            console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

            setTimeout(() => {
                const token = localStorage.getItem('access_token') || '';
                this.connect(this.workspaceId!, token);
            }, delay);
        }
    }

    disconnect() {
        this.stopHeartbeat();
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        this.listeners.clear();
        this.workspaceId = null;
    }

    isConnected(): boolean {
        return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
    }
}

export const wsService = new WebSocketService();
