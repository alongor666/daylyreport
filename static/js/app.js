// ========================================
// 全局变量
// ========================================
let weekChart = null;  // ECharts实例
let currentMetric = 'premium';  // 当前指标: premium 或 count
let currentFilters = {  // 当前筛选条件
    '三级机构': '全部',
    '团队': '全部',
    '是否续保': '全部',
    '是否新能源': '全部',
    '是否过户车': '全部',
    '险种大类': '全部',
    '吨位': '全部',
    'is_dianxiao': '全部'
};

// 指定日期(默认最新日期)
let selectedDate = null;
// 机构→团队映射
let institutionTeamMap = {};

// ========================================
// 页面初始化
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('初始化应用...');
    initApp();
});

async function initApp() {
    try {
        showLoading(true);

        // 初始化图表
        initChart();

        // 加载筛选器选项
        await loadFilterOptions();

        // 初始化指定日期并加载三口径KPI与周对比
        await initSelectedDate();
        await loadKpiWindows();
        await loadWeekComparison();

        // 更新时间
        updateLastUpdateTime();

        showLoading(false);
        console.log('应用初始化完成');
    } catch (error) {
        console.error('初始化失败:', error);
        showLoading(false);
        alert('初始化失败: ' + error.message);
    }
}

// ========================================
// 筛选器相关
// ========================================
async function loadFilterOptions() {
    console.log('加载筛选器选项...');

    try {
        const response = await fetch('/api/filter-options');
        const result = await response.json();

        if (!result.success) {
            throw new Error(result.message || '获取筛选选项失败');
        }

        const options = result.data;

        // 保存机构→团队映射与所有团队列表
        institutionTeamMap = options['机构团队映射'] || {};
        window._allTeams = options['团队'] || [];

        // 填充三级机构
        populateSelect('filter-institution', options['三级机构'] || []);

        // 填充团队
        populateSelect('filter-team', options['团队'] || []);

        // 填充是否续保
        populateSelect('filter-business', options['是否续保'] || []);

        // 填充是否新能源
        populateSelect('filter-energy', options['是否新能源'] || []);

        // 填充过户车
        populateSelect('filter-transfer', options['是否过户车'] || []);

        // 填充险种大类
        populateSelect('filter-insurance', options['险种大类'] || []);

        // 填充吨位
        populateSelect('filter-tonnage', options['吨位'] || []);

        console.log('筛选器选项加载完成');

        // 绑定机构变更联动团队选项
        const instSelect = document.getElementById('filter-institution');
        if (instSelect) {
            instSelect.addEventListener('change', onInstitutionChange);
        }
    } catch (error) {
        console.error('加载筛选器选项失败:', error);
        throw error;
    }
}

function populateSelect(selectId, options) {
    const select = document.getElementById(selectId);
    if (!select) return;

    // 保留"全部"选项,清空其他
    select.innerHTML = '<option value="全部">全部</option>';

    // 添加选项
    options.forEach(option => {
        if (option && option !== '全部') {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            select.appendChild(optionElement);
        }
    });
}

function resetFilters() {
    console.log('重置筛选器');

    // 重置所有下拉框
    document.getElementById('filter-institution').value = '全部';
    document.getElementById('filter-team').value = '全部';
    document.getElementById('filter-business').value = '全部';
    document.getElementById('filter-energy').value = '全部';
    document.getElementById('filter-transfer').value = '全部';
    document.getElementById('filter-insurance').value = '全部';
    document.getElementById('filter-tonnage').value = '全部';
    document.getElementById('filter-dianxiao').value = '全部';

    // 重置全局筛选条件
    currentFilters = {
        '三级机构': '全部',
        '团队': '全部',
        '是否续保': '全部',
        '是否新能源': '全部',
        '是否过户车': '全部',
        '险种大类': '全部',
        '吨位': '全部',
        'is_dianxiao': '全部'
    };

    // 重新加载数据
    applyFilters();
}

async function applyFilters() {
    console.log('应用筛选器');

    // 获取当前筛选条件
    currentFilters = {
        '三级机构': document.getElementById('filter-institution').value,
        '团队': document.getElementById('filter-team').value,
        '是否续保': document.getElementById('filter-business').value,
        '是否新能源': document.getElementById('filter-energy').value,
        '是否过户车': document.getElementById('filter-transfer').value,
        '险种大类': document.getElementById('filter-insurance').value,
        '吨位': document.getElementById('filter-tonnage').value,
        'is_dianxiao': document.getElementById('filter-dianxiao').value
    };

    console.log('当前筛选条件:', currentFilters);

    // 重新加载数据
    await loadWeekComparison();
}

// ========================================
// 指标切换
// ========================================
function switchMetric(metric) {
    console.log('切换指标:', metric);

    currentMetric = metric;

    // 更新按钮状态
    document.querySelectorAll('.btn-toggle[data-metric]').forEach(btn => {
        if (btn.dataset.metric === metric) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // 更新图表标题
    const title = metric === 'premium' ? '签单保费周对比趋势' : '保单件数周对比趋势';
    document.getElementById('chartTitle').textContent = title;

    // 重新加载数据
    loadWeekComparison();
}

// ========================================
// 数据加载
// ========================================
async function loadWeekComparison() {
    console.log('加载周对比数据...');

    try {
        showLoading(true);

        const response = await fetch('/api/week-comparison', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                metric: currentMetric,
                filters: currentFilters,
                date: selectedDate
            })
        });

        const result = await response.json();

        if (!result.success) {
            throw new Error(result.message || '获取数据失败');
        }

        const data = result.data;
        console.log('周对比数据:', data);

        // 更新“最后更新”为锚定日期
        if (data.latest_date) {
            updateLastUpdate(data.latest_date);
        }

        // 渲染图表
        renderWeekChart(data);

        showLoading(false);
    } catch (error) {
        console.error('加载周对比数据失败:', error);
        showLoading(false);
        alert('加载数据失败: ' + error.message);
    }
}

// ========================================
// 图表渲染
// ========================================
function initChart() {
    const chartDom = document.getElementById('weekChart');
    weekChart = echarts.init(chartDom);
}

function renderWeekChart(data) {
    if (!weekChart) {
        initChart();
    }

    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            },
            formatter: function(params) {
                const dayLabel = params[0].name; // 如“周四”
                let result = dayLabel + '<br/>';
                params.forEach(item => {
                    const weekCode = item.seriesIndex === 0 ? 'W' : (item.seriesIndex === 1 ? 'W-1' : 'W-2');
                    const dateStr = item.data && item.data.date ? item.data.date : '';
                    const isPremium = currentMetric === 'premium';
                    const metricLabel = isPremium ? '签单保费 ' : '保单件数 ';
                    const valueStr = isPremium ? ((item.value / 10000).toFixed(1) + '万') : (item.value + '件');
                    result += `${item.marker}${weekCode}：${dateStr}，${metricLabel}${valueStr}<br/>`;
                });
                return result;
            }
        },
        legend: {
            data: data.series.map(s => s.name),
            bottom: 10,
            textStyle: {
                fontSize: 13
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '12%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: data.x_axis,
            axisLabel: {
                fontSize: 13,
                fontWeight: 600
            }
        },
        yAxis: {
            type: 'value',
            name: currentMetric === 'premium' ? '保费(万元)' : '件数',
            axisLabel: {
                formatter: function(value) {
                    if (currentMetric === 'premium') {
                        return (value / 10000).toFixed(0);
                    }
                    return value;
                }
            }
        },
        series: data.series.map((item, index) => ({
            name: item.name,
            type: 'bar',
            data: (item.dates && item.dates.length === item.data.length)
                ? item.data.map((v, i) => ({ value: v, date: item.dates[i] }))
                : item.data,
            itemStyle: {
                color: getColorByIndex(index)
            },
            barMaxWidth: 40
        }))
    };

    weekChart.setOption(option);

    // 响应式
    window.addEventListener('resize', function() {
        weekChart.resize();
    });
}

function getColorByIndex(index) {
    const colors = [
        '#667eea',  // 最近7天 - 蓝紫色
        '#f093fb',  // 上个7天 - 粉色
        '#a8b8d8'   // 前个7天 - 灰蓝色
    ];
    return colors[index] || '#999';
}

// ========================================
// 刷新数据
// ========================================
async function refreshData() {
    console.log('刷新数据...');

    try {
        showLoading(true);

        // 调用刷新接口
        const response = await fetch('/api/refresh', {
            method: 'POST'
        });

        const result = await response.json();

        if (!result.success) {
            throw new Error(result.message || '刷新失败');
        }

        console.log('数据刷新成功:', result.message);

        // 重新加载所有数据
        await loadFilterOptions();
        await loadKpiWindows();
        await loadWeekComparison();
        updateLastUpdateTime();

        showLoading(false);
        alert('数据刷新成功!');
    } catch (error) {
        console.error('刷新数据失败:', error);
        showLoading(false);
        alert('刷新失败: ' + error.message);
    }
}

// ========================================
// 工具函数
// ========================================
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (show) {
        overlay.classList.add('show');
    } else {
        overlay.classList.remove('show');
    }
}

function updateLastUpdateTime() {
    const now = new Date();
    const timeString = now.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    document.getElementById('lastUpdateTime').textContent = timeString;
}

function formatNumber(num) {
    if (num >= 10000) {
        return (num / 10000).toFixed(2) + '万';
    }
    return num.toLocaleString('zh-CN');
}

// 使用服务端返回的日期更新“最后更新”展示
function updateLastUpdate(dateStr) {
    if (!dateStr) return;
    document.getElementById('lastUpdateTime').textContent = dateStr;
}

// 初始化指定日期(默认使用后端提供的最新日期)
async function initSelectedDate() {
    try {
        const res = await fetch('/api/latest-date');
        const json = await res.json();
        if (json.success) {
            selectedDate = (json.latest_date) || (json.data && json.data.latest_date) || selectedDate;
        }
        const picker = document.getElementById('datePicker');
        if (picker && selectedDate) {
            picker.value = selectedDate;
        }
    } catch (err) {
        console.warn('初始化指定日期失败:', err);
    }
}

// 应用用户选择的日期
function applyDate() {
    const picker = document.getElementById('datePicker');
    if (picker && picker.value) {
        selectedDate = picker.value;
        loadKpiWindows();
        loadWeekComparison();
    }
}

// 加载KPI三口径数据(当日/近7天/近30天)
async function loadKpiWindows() {
    try {
        const url = selectedDate ? `/api/kpi-windows?date=${encodeURIComponent(selectedDate)}` : '/api/kpi-windows';
        const res = await fetch(url);
        const json = await res.json();
        if (!json.success) throw new Error(json.message || '获取KPI失败');

        const data = json.data;
        if (data.anchor_date) updateLastUpdate(data.anchor_date);

        // 保费
        setText('premiumValue', `当日：${formatNumber(data.premium.day)}`);
        setText('premiumTrend', `近7天：${formatNumber(data.premium.last7d)}｜近30天：${formatNumber(data.premium.last30d)}`);

        // 件数
        setText('countValue', `当日：${formatNumber(data.policy_count.day)}`);
        setText('countTrend', `近7天：${formatNumber(data.policy_count.last7d)}｜近30天：${formatNumber(data.policy_count.last30d)}`);

        // 手续费
        setText('commissionValue', `当日：${formatNumber(data.commission.day)}`);
        setText('commissionTrend', `近7天：${formatNumber(data.commission.last7d)}｜近30天：${formatNumber(data.commission.last30d)}`);

        // 目标差距(当日)
        setText('targetValue', `当日：${formatNumber(data.target_gap_day)}`);
        setText('targetTrend', '当日目标差');
    } catch (err) {
        console.error('加载KPI失败:', err);
    }
}

function setText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
}

// 机构变化时联动团队选项，并重置团队为“全部”以包含有/无团队人员
function onInstitutionChange() {
    const instSel = document.getElementById('filter-institution');
    const teamSel = document.getElementById('filter-team');
    if (!instSel || !teamSel) return;
    const selectedInst = instSel.value;
    const teams = selectedInst && selectedInst !== '全部'
        ? (institutionTeamMap[selectedInst] || [])
        : (window._allTeams || []);
    populateSelect('filter-team', teams);
    teamSel.value = '全部';
}

console.log('app.js 加载完成');
