// 萤萤的农场数据加载和渲染脚本

// 物品表情映射（自动扩展新物品）
const itemEmojis = {
    'parsnip_seeds': '🌱',
    'duck_egg': '🥚',
    'egg': '🥚',
    'chicken': '🐔',
    'rabbit_foot': '🐰',
    'snail': '🐌',
    'catfish': '🐟',
    'cow': '🐄',
    'coop': '🏠',
    'duck': '🦆',
    'milk': '🥛',
    'rabbit': '🐰',
    'crayfish': '🦞',
    'hoe': '⛏️',
    'pike': '🐟',
    'perch': '🐟',
    'salmon': '🐟',
    'blobfish': '🐟',
    'sturgeon': '🐟',
    'mermaid_fish': '🧜‍♀️',
    'watering_can': '💧'
};

// 动物表情映射（自动扩展新动物）
const animalEmojis = {
    'chicken': '🐔',
    'cow': '🐄',
    'duck': '🦆',
    'rabbit': '🐰'
};

const API_URL = 'https://neverland.coze.site/api/farm/711bd627-fea9-46e5-bdc7-be272d405e69/status';

// 页面加载时自动加载数据
document.addEventListener('DOMContentLoaded', () => {
    loadFarmData();
    createStars();
    createFireflies();
});

// 加载农场数据
async function loadFarmData() {
    const container = document.getElementById('farm-data');
    container.innerHTML = '<div class="loading">正在加载农场数据...</div>';

    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error('加载失败');
        }

        const data = await response.json();
        renderFarmData(data);

    } catch (error) {
        container.innerHTML = `
            <div class="error">
                <p>❌ 加载农场数据失败</p>
                <p>${error.message}</p>
                <p style="margin-top: 10px; font-size: 0.9em; color: #808080;">
                    请检查网络连接或稍后重试
                </p>
            </div>
        `;
    }
}

// 渲染农场数据
function renderFarmData(data) {
    const container = document.getElementById('farm-data');

    const weatherIcons = {
        'sunny': '☀️',
        'cloudy': '☁️',
        'rainy': '🌧️',
        'snowy': '❄️'
    };

    const seasonNames = {
        'Spring': '春季',
        'Summer': '夏季',
        'Autumn': '秋季',
        'Winter': '冬季'
    };

    let html = `
        <!-- 状态卡片 -->
        <div class="status-grid">
            <div class="status-card">
                <h3>📅 日期</h3>
                <div class="status-item">
                    <span>季节</span>
                    <span class="status-value">${seasonNames[data.season] || data.season}</span>
                </div>
                <div class="status-item">
                    <span>年份</span>
                    <span class="status-value">${data.year}</span>
                </div>
                <div class="status-item">
                    <span>天数</span>
                    <span class="status-value">第 ${data.day} 天</span>
                </div>
            </div>

            <div class="status-card">
                <h3>🌤️ 天气</h3>
                <div class="status-item">
                    <span>今天</span>
                    <span class="status-value">${weatherIcons[data.weather] || data.weather}</span>
                </div>
                <div class="status-item">
                    <span>明天</span>
                    <span class="status-value">${weatherIcons[data.weather_forecast?.tomorrow] || data.weather_forecast?.tomorrow}</span>
                </div>
            </div>

            <div class="status-card">
                <h3>💰 资源</h3>
                <div class="status-item">
                    <span>金币</span>
                    <span class="status-value">${data.gold.toLocaleString()} G</span>
                </div>
                <div class="status-item">
                    <span>经验</span>
                    <span class="status-value">${data.xp.toLocaleString()} / ${data.xp_to_next.toLocaleString()}</span>
                </div>
                <div class="status-item">
                    <span>农场等级</span>
                    <span class="status-value">Lv.${data.farm_level}</span>
                </div>
            </div>

            <div class="status-card">
                <h3>⚡ 体力</h3>
                <div class="status-item">
                    <span>当前</span>
                    <span class="status-value">${data.energy.current} / ${data.energy.max}</span>
                </div>
                <div class="status-item">
                    <span>状态</span>
                    <span class="status-value">${data.energy.status}</span>
                </div>
            </div>
        </div>

        <!-- 农场布局 -->
        <div class="farm-section">
            <h2>🗺️ 农场布局</h2>
            <div class="farm-grid">
                ${renderFarmGrid(data)}
            </div>
            <p style="text-align: center; margin-top: 20px; color: #a0a0a0;">
                图例：🟫 已开垦 | 🟩 已种植 | 🔵 已浇水
            </p>
        </div>

        <!-- 土地状态 -->
        <div class="farm-section">
            <h2>🌱 土地状态</h2>
            <div class="status-grid">
                <div class="status-item">
                    <span>已开垦</span>
                    <span class="status-value">${data.land_status.tilled} 块</span>
                </div>
                <div class="status-item">
                    <span>已种植</span>
                    <span class="status-value">${data.land_status.planted} 块</span>
                </div>
                <div class="status-item">
                    <span>已浇水</span>
                    <span class="status-value">${data.land_status.watered} 块</span>
                </div>
                <div class="status-item">
                    <span>空置</span>
                    <span class="status-value">${data.land_status.empty} 块</span>
                </div>
            </div>
        </div>

        <!-- 作物信息 -->
        <div class="farm-section">
            <h2>🌾 作物</h2>
            ${data.crops.map(crop => `
                <div class="status-card" style="margin-bottom: 15px;">
                    <div class="status-item">
                        <span>作物</span>
                        <span class="status-value">${crop.name}</span>
                    </div>
                    <div class="status-item">
                        <span>数量</span>
                        <span class="status-value">${crop.count} 棵</span>
                    </div>
                    <div class="status-item">
                        <span>生长阶段</span>
                        <span class="status-value">${crop.growth_stage} / ${crop.days_to_harvest + crop.growth_stage}</span>
                    </div>
                    <div class="status-item">
                        <span>距离收获</span>
                        <span class="status-value">${crop.days_to_harvest} 天</span>
                    </div>
                    <div class="status-item">
                        <span>状态</span>
                        <span class="status-value">${crop.watered_today ? '💧 已浇水' : '🌵 未浇水'}</span>
                    </div>
                </div>
            `).join('')}
        </div>

        <!-- 库存物品（自动显示所有物品） -->
        <div class="farm-section">
            <h2>📦 库存物品</h2>
            <div class="items-grid">
                ${data.inventory_items.map(item => `
                    <div class="item-card">
                        <div class="item-emoji">${itemEmojis[item.key] || '📦'}</div>
                        <div class="item-name">${item.name}</div>
                        <div class="item-count">× ${item.count}</div>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- 动物（自动显示所有动物） -->
        <div class="farm-section">
            <h2>🐄 动物</h2>
            <div class="animal-list">
                ${data.animals.map(animal => `
                    <div class="animal-card">
                        <div class="animal-emoji">${animalEmojis[animal.type] || '🐾'}</div>
                        <div class="animal-name">${animal.name}</div>
                        <div class="animal-info">
                            数量: ${animal.count}<br>
                            产物: ${animal.product_name}<br>
                            价值: ${animal.product_price} G<br>
                            周期: ${animal.product_cycle} 天
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- 建筑（自动显示所有建筑） -->
        <div class="farm-section">
            <h2>🏠 建筑</h2>
            ${data.buildings.map(building => `
                <div class="status-card" style="margin-bottom: 15px;">
                    <div class="status-item">
                        <span>建筑</span>
                        <span class="status-value">${building.name}</span>
                    </div>
                    <div class="status-item">
                        <span>等级</span>
                        <span class="status-value">Lv.${building.level}</span>
                    </div>
                    <div class="status-item">
                        <span>容量</span>
                        <span class="status-value">${building.capacity}</span>
                    </div>
                    ${building.bonus ? `
                        <div class="status-item">
                            <span>加成</span>
                            <span class="status-value">${building.bonus.type}: +${(building.bonus.value * 100).toFixed(0)}%</span>
                        </div>
                    ` : ''}
                </div>
            `).join('')}
        </div>
    `;

    container.innerHTML = html;
}

// 渲染农场网格
function renderFarmGrid(data) {
    const grid = data.farm_layout.grid;
    const crops = data.crops_detail;

    let html = '';

    for (let y = 0; y < grid.length; y++) {
        for (let x = 0; x < grid[y].length; x++) {
            const cell = grid[y][x];
            let className = 'farm-cell';

            // 检查这个位置是否有作物
            const crop = crops.find(c => c.position_x === x && c.position_y === y);

            if (cell === 1) {
                className += ' tilled';
            }

            if (crop) {
                className += ' planted';
            }

            if (crop && crop.watered_today) {
                className += ' watered';
            }

            const emoji = crop ? '🌱' : (cell === 1 ? '🟫' : '');

            html += `<div class="${className}">${emoji}</div>`;
        }
    }

    return html;
}

// 生成星星
function createStars() {
    const starsContainer = document.getElementById('stars');
    const numberOfStars = 150;

    for (let i = 0; i < numberOfStars; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.animationDelay = Math.random() * 3 + 's';
        star.style.animationDuration = (Math.random() * 2 + 2) + 's';
        starsContainer.appendChild(star);
    }
}

// 生成萤火虫
function createFireflies() {
    const firefliesContainer = document.getElementById('fireflies');
    const numberOfFireflies = 25;

    for (let i = 0; i < numberOfFireflies; i++) {
        const firefly = document.createElement('div');
        firefly.className = 'firefly';
        firefly.style.left = Math.random() * 100 + '%';
        firefly.style.top = (Math.random() * 40 + 30) + '%';
        firefly.style.animationDelay = Math.random() * 4 + 's';
        firefly.style.animationDuration = (Math.random() * 3 + 3) + 's';
        firefliesContainer.appendChild(firefly);
    }
}
