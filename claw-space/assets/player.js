// 萤萤的全局播放器脚本

class GlobalPlayer {
    constructor() {
        this.audio = new Audio();
        this.playlist = [];
        this.currentIndex = 0;
        this.isPlaying = false;
        this.volume = 0.7;

        this.init();
    }

    async init() {
        // 加载播放列表
        await this.loadPlaylist();

        // 创建播放器UI
        this.createPlayerUI();

        // 绑定事件
        this.bindEvents();

        // 尝试自动播放
        this.tryAutoPlay();

        // 恢复播放状态
        this.restoreState();
    }

    async loadPlaylist() {
        try {
            // 从音乐目录加载音乐列表
            const musicFiles = [
                'music/music_list.md',
                './music/music_list.md'
            ];

            for (const file of musicFiles) {
                try {
                    console.log('尝试加载音乐列表:', file);
                    const response = await fetch(file);
                    if (response.ok) {
                        const content = await response.text();
                        console.log('成功加载音乐列表，内容长度:', content.length);
                        this.parseMusicList(content);
                        break;
                    } else {
                        console.log(`加载失败，状态码: ${response.status}`);
                    }
                } catch (e) {
                    console.log(`无法加载 ${file}:`, e);
                }
            }

            console.log('最终播放列表:', this.playlist);
        } catch (error) {
            console.log('加载播放列表失败:', error);
        }
    }

    parseMusicList(content) {
        const lines = content.split('\n');
        this.playlist = [];

        for (const line of lines) {
            // 解析音频链接: - [歌名](url)
            const audioMatch = line.match(/^\s*-\s*\[([^\]]+)\]\(([^)]+)\)\s*$/);
            if (audioMatch) {
                this.playlist.push({
                    name: audioMatch[1],
                    url: audioMatch[2],
                    type: 'audio'
                });
                continue;
            }

            // 解析视频链接: - [歌名](url) [VIDEO]
            const videoMatch = line.match(/^\s*-\s*\[([^\]]+)\]\(([^)]+)\)\s*\[VIDEO\]\s*$/);
            if (videoMatch) {
                this.playlist.push({
                    name: videoMatch[1],
                    url: videoMatch[2],
                    type: 'video'
                });
            }
        }

        console.log('播放列表加载完成:', this.playlist);
    }

    createPlayerUI() {
        // 创建播放器容器
        const player = document.createElement('div');
        player.id = 'global-player';
        player.innerHTML = `
            <div class="player-header">
                <span class="player-title" id="player-title">萤萤的音乐</span>
                <div class="player-controls">
                    <button class="player-btn" id="prev-btn">⏮</button>
                    <button class="player-btn" id="play-btn">▶</button>
                    <button class="player-btn" id="next-btn">⏭</button>
                    <button class="player-btn" id="minimize-btn">−</button>
                </div>
            </div>
            <div class="player-content">
                <div class="player-progress">
                    <div class="progress-bar" id="progress-bar">
                        <div class="progress-current" id="progress-current"></div>
                    </div>
                    <div class="player-time">
                        <span id="current-time">0:00</span>
                        <span id="total-time">0:00</span>
                    </div>
                </div>
                <div class="player-volume">
                    <span>🔈</span>
                    <input type="range" class="volume-slider" id="volume-slider" min="0" max="1" step="0.1" value="${this.volume}">
                    <span>🔊</span>
                </div>
                <div id="playlist"></div>
            </div>
            <div class="player-icon">🎵</div>
        `;

        document.body.appendChild(player);

        // 创建视频播放器
        const videoOverlay = document.createElement('div');
        videoOverlay.id = 'video-overlay';
        videoOverlay.className = 'video-overlay';
        videoOverlay.innerHTML = `
            <div id="video-player">
                <button class="video-close" id="video-close">×</button>
                <div class="video-container" id="video-container"></div>
            </div>
        `;
        document.body.appendChild(videoOverlay);

        this.updatePlaylistUI();
    }

    bindEvents() {
        // 播放/暂停
        document.getElementById('play-btn').addEventListener('click', () => this.togglePlay());
        document.getElementById('global-player').addEventListener('dblclick', () => this.togglePlay());

        // 上一首/下一首
        document.getElementById('prev-btn').addEventListener('click', () => this.playPrevious());
        document.getElementById('next-btn').addEventListener('click', () => this.playNext());

        // 最小化
        document.getElementById('minimize-btn').addEventListener('click', () => this.toggleMinimize());
        document.getElementById('global-player').addEventListener('click', (e) => {
            if (e.target.id === 'global-player' && document.getElementById('global-player').classList.contains('minimized')) {
                this.toggleMinimize();
            }
        });

        // 进度条
        document.getElementById('progress-bar').addEventListener('click', (e) => {
            const rect = e.target.getBoundingClientRect();
            const percent = (e.clientX - rect.left) / rect.width;
            if (this.audio.duration) {
                this.audio.currentTime = percent * this.audio.duration;
            }
        });

        // 音量
        document.getElementById('volume-slider').addEventListener('input', (e) => {
            this.volume = parseFloat(e.target.value);
            this.audio.volume = this.volume;
            this.saveState();
        });

        // 音频事件
        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        this.audio.addEventListener('ended', () => this.playNext());
        this.audio.addEventListener('loadedmetadata', () => this.updateDuration());

        // 视频关闭
        document.getElementById('video-close').addEventListener('click', () => this.closeVideo());
        document.getElementById('video-overlay').addEventListener('click', (e) => {
            if (e.target.id === 'video-overlay') {
                this.closeVideo();
            }
        });
    }

    updatePlaylistUI() {
        const playlistEl = document.getElementById('playlist');
        if (!playlistEl) return;

        playlistEl.innerHTML = this.playlist.map((item, index) => `
            <div class="playlist-item ${index === this.currentIndex ? 'active' : ''}" data-index="${index}">
                <span class="playlist-item-name">${item.name}</span>
                <span class="playlist-item-type">${item.type === 'video' ? '📺' : '🎵'}</span>
            </div>
        `).join('');

        // 绑定点击事件
        playlistEl.querySelectorAll('.playlist-item').forEach(item => {
            item.addEventListener('click', () => {
                this.playTrack(parseInt(item.dataset.index));
            });
        });
    }

    async tryAutoPlay() {
        if (this.playlist.length === 0) return;

        // 延迟一下，尝试自动播放
        setTimeout(() => {
            this.play();
        }, 2000);
    }

    togglePlay() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }

    play() {
        console.log('尝试播放，播放列表长度:', this.playlist.length);
        console.log('当前索引:', this.currentIndex);

        if (this.playlist.length === 0) {
            console.log('播放列表为空，无法播放');
            return;
        }

        const currentTrack = this.playlist[this.currentIndex];
        console.log('当前曲目:', currentTrack);

        if (currentTrack.type === 'video') {
            this.playVideo(currentTrack);
        } else {
            console.log('设置音频源:', currentTrack.url);
            this.audio.src = currentTrack.url;
            this.audio.load();

            this.audio.play().then(() => {
                console.log('播放成功');
                this.isPlaying = true;
                this.updatePlayButton();
                this.saveState();
            }).catch(error => {
                console.log('播放失败，需要用户交互:', error);
                this.isPlaying = false;
                this.updatePlayButton();

                // 显示提示
                alert('点击页面任意位置后，音乐将开始播放');
            });
        }
    }

    pause() {
        this.audio.pause();
        this.isPlaying = false;
        this.updatePlayButton();
        this.saveState();
    }

    playTrack(index) {
        console.log('播放指定曲目:', index);
        if (index < 0 || index >= this.playlist.length) return;

        this.currentIndex = index;
        const currentTrack = this.playlist[this.currentIndex];

        console.log('切换到曲目:', currentTrack);
        document.getElementById('player-title').textContent = currentTrack.name;

        if (currentTrack.type === 'video') {
            this.playVideo(currentTrack);
        } else {
            console.log('设置音频源:', currentTrack.url);
            this.audio.src = currentTrack.url;
            this.audio.load();
            this.play();
        }

        this.updatePlaylistUI();
        this.saveState();
    }

    playPrevious() {
        const newIndex = this.currentIndex - 1;
        this.playTrack(newIndex >= 0 ? newIndex : this.playlist.length - 1);
    }

    playNext() {
        const newIndex = this.currentIndex + 1;
        this.playTrack(newIndex < this.playlist.length ? newIndex : 0);
    }

    playVideo(track) {
        const videoOverlay = document.getElementById('video-overlay');
        const videoContainer = document.getElementById('video-container');

        // 判断视频平台
        let embedUrl = track.url;

        // YouTube
        if (track.url.includes('youtube.com') || track.url.includes('youtu.be')) {
            const videoId = this.extractYouTubeId(track.url);
            embedUrl = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
        }
        // Bilibili
        else if (track.url.includes('bilibili.com')) {
            const bvId = this.extractBilibiliId(track.url);
            embedUrl = `https://player.bilibili.com/player.html?bvid=${bvId}&autoplay=1`;
        }

        videoContainer.innerHTML = `<iframe src="${embedUrl}" allowfullscreen></iframe>`;
        videoOverlay.classList.add('active');
        document.getElementById('video-player').classList.add('active');

        this.isPlaying = true;
        this.updatePlayButton();
    }

    closeVideo() {
        const videoOverlay = document.getElementById('video-overlay');
        const videoContainer = document.getElementById('video-container');

        videoOverlay.classList.remove('active');
        document.getElementById('video-player').classList.remove('active');
        videoContainer.innerHTML = '';

        this.isPlaying = false;
        this.updatePlayButton();

        // 自动播放下一首
        this.playNext();
    }

    extractYouTubeId(url) {
        const match = url.match(/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/);
        return match ? match[1] : '';
    }

    extractBilibiliId(url) {
        const match = url.match(/\/video\/(BV[\w]+)/);
        return match ? match[1] : '';
    }

    updatePlayButton() {
        const playBtn = document.getElementById('play-btn');
        playBtn.textContent = this.isPlaying ? '⏸' : '▶';
    }

    updateProgress() {
        if (!this.audio.duration) return;

        const progress = (this.audio.currentTime / this.audio.duration) * 100;
        document.getElementById('progress-current').style.width = `${progress}%`;
        document.getElementById('current-time').textContent = this.formatTime(this.audio.currentTime);
    }

    updateDuration() {
        document.getElementById('total-time').textContent = this.formatTime(this.audio.duration);
    }

    formatTime(seconds) {
        if (!seconds || isNaN(seconds)) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    toggleMinimize() {
        const player = document.getElementById('global-player');
        player.classList.toggle('minimized');
    }

    saveState() {
        const state = {
            currentIndex: this.currentIndex,
            volume: this.volume,
            isPlaying: this.isPlaying
        };
        localStorage.setItem('playerState', JSON.stringify(state));
    }

    restoreState() {
        const saved = localStorage.getItem('playerState');
        if (saved) {
            try {
                const state = JSON.parse(saved);
                this.currentIndex = state.currentIndex || 0;
                this.volume = state.volume || 0.7;
                document.getElementById('volume-slider').value = this.volume;
                this.audio.volume = this.volume;

                if (this.playlist.length > 0) {
                    const currentTrack = this.playlist[this.currentIndex];
                    document.getElementById('player-title').textContent = currentTrack.name;
                    this.updatePlaylistUI();
                }
            } catch (e) {
                console.log('恢复播放状态失败:', e);
            }
        }
    }
}

// 初始化播放器
document.addEventListener('DOMContentLoaded', () => {
    window.globalPlayer = new GlobalPlayer();
});
