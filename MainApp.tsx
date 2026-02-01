import React, { useEffect, useState } from 'react';
import { workspaceAPI, channelAPI, messageAPI, userAPI } from '@/services/api';
import { wsService } from '@/services/websocket';
import './MainApp.css';

export const MainApp: React.FC = () => {
    const [workspaces, setWorkspaces] = useState<any[]>([]);
    const [currentWorkspace, setCurrentWorkspace] = useState<any>(null);
    const [channels, setChannels] = useState<any[]>([]);
    const [currentChannel, setCurrentChannel] = useState<any>(null);
    const [messages, setMessages] = useState<any[]>([]);
    const [messageInput, setMessageInput] = useState('');
    const [user, setUser] = useState<any>(null);

    useEffect(() => {
        loadUser();
        loadWorkspaces();
    }, []);

    useEffect(() => {
        if (currentWorkspace) {
            loadChannels(currentWorkspace.id);
            const token = localStorage.getItem('access_token') || '';
            wsService.connect(currentWorkspace.id, token);

            wsService.on('message.new', (data) => {
                if (data.data.channel_id === currentChannel?.id) {
                    setMessages((prev) => [...prev, data.data]);
                }
            });

            return () => {
                wsService.disconnect();
            };
        }
    }, [currentWorkspace]);

    useEffect(() => {
        if (currentChannel) {
            loadMessages(currentChannel.id);
        }
    }, [currentChannel]);

    const loadUser = async () => {
        try {
            const response = await userAPI.getMe();
            setUser(response.data);
        } catch (error) {
            console.error('Failed to load user:', error);
        }
    };

    const loadWorkspaces = async () => {
        try {
            const response = await workspaceAPI.list();
            setWorkspaces(response.data);
            if (response.data.length > 0) {
                setCurrentWorkspace(response.data[0]);
            }
        } catch (error) {
            console.error('Failed to load workspaces:', error);
        }
    };

    const loadChannels = async (workspaceId: string) => {
        try {
            const response = await channelAPI.list(workspaceId);
            setChannels(response.data);
            if (response.data.length > 0) {
                setCurrentChannel(response.data[0]);
            }
        } catch (error) {
            console.error('Failed to load channels:', error);
        }
    };

    const loadMessages = async (channelId: string) => {
        try {
            const response = await messageAPI.list({ channel_id: channelId, limit: 50 });
            setMessages(response.data.reverse());
        } catch (error) {
            console.error('Failed to load messages:', error);
        }
    };

    const sendMessage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!messageInput.trim() || !currentChannel || !currentWorkspace) return;

        try {
            await messageAPI.send(currentWorkspace.id, {
                channel_id: currentChannel.id,
                content: messageInput,
            });
            setMessageInput('');
        } catch (error) {
            console.error('Failed to send message:', error);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
    };

    return (
        <div className="main-app">
            {/* Sidebar */}
            <div className="sidebar glass">
                <div className="sidebar-header">
                    <h2>Forensic Messenger</h2>
                </div>

                <div className="workspace-section">
                    <h3 className="section-title">Workspaces</h3>
                    {workspaces.map((ws) => (
                        <div
                            key={ws.id}
                            className={`workspace-item ${currentWorkspace?.id === ws.id ? 'active' : ''}`}
                            onClick={() => setCurrentWorkspace(ws)}
                        >
                            <div className="workspace-icon">{ws.name[0]}</div>
                            <span>{ws.name}</span>
                        </div>
                    ))}
                </div>

                <div className="channel-section">
                    <h3 className="section-title">Channels</h3>
                    {channels.map((channel) => (
                        <div
                            key={channel.id}
                            className={`channel-item ${currentChannel?.id === channel.id ? 'active' : ''}`}
                            onClick={() => setCurrentChannel(channel)}
                        >
                            <span className="channel-hash">#</span>
                            <span>{channel.name}</span>
                        </div>
                    ))}
                </div>

                <div className="user-section">
                    {user && (
                        <div className="user-info">
                            <div className="user-avatar">{user.full_name[0]}</div>
                            <div className="user-details">
                                <div className="user-name">{user.full_name}</div>
                                <div className="user-status">
                                    <span className="status-dot status-online"></span>
                                    Online
                                </div>
                            </div>
                            <button className="btn-logout" onClick={handleLogout}>
                                Logout
                            </button>
                        </div>
                    )}
                </div>
            </div>

            {/* Main Content */}
            <div className="main-content">
                {/* Channel Header */}
                <div className="channel-header glass">
                    <div className="channel-info">
                        <h2>
                            <span className="channel-hash">#</span>
                            {currentChannel?.name || 'Select a channel'}
                        </h2>
                        {currentChannel?.description && (
                            <p className="text-secondary text-sm">{currentChannel.description}</p>
                        )}
                    </div>
                </div>

                {/* Messages */}
                <div className="messages-container">
                    {messages.map((msg) => (
                        <div key={msg.id} className="message animate-slide-in">
                            <div className="message-avatar">{msg.user_id[0]}</div>
                            <div className="message-content">
                                <div className="message-header">
                                    <span className="message-author">{msg.user_id}</span>
                                    <span className="message-time text-xs text-muted">
                                        {new Date(msg.created_at).toLocaleTimeString()}
                                    </span>
                                </div>
                                <div className="message-text">{msg.content}</div>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Message Input */}
                <div className="message-input-container glass">
                    <form onSubmit={sendMessage} className="message-form">
                        <input
                            type="text"
                            value={messageInput}
                            onChange={(e) => setMessageInput(e.target.value)}
                            placeholder={`Message #${currentChannel?.name || 'channel'}`}
                            className="message-input"
                        />
                        <button type="submit" className="btn btn-primary">
                            Send
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};
