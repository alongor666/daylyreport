// 说明：前端逻辑，负责从本地API拉取数据并渲染ECharts图表。

/**
 * 初始化：绑定事件、加载元信息并触发默认数据渲染。
 */
async function init() {
  const meta = await fetchJson('/api/meta');
  const metaEl = document.getElementById('meta');
  if (meta && meta.start && meta.end) {
    document.getElementById('startDate').value = meta.start;
    document.getElementById('endDate').value = meta.end;
    metaEl.textContent = `文件数：${meta.file_count}，目录：${meta.input_dir}`;
  } else {
    metaEl.textContent = '未识别到日期范围或文件，请检查目录';
  }

  document.getElementById('refreshBtn').addEventListener('click', renderAll);
  document.getElementById('qualityBtn').addEventListener('click', openQuality);
  document.getElementById('qualityClose').addEventListener('click', closeQuality);
  // 增强关闭交互：点击遮罩关闭、ESC键关闭
  const modalEl = document.getElementById('qualityModal');
  if (modalEl) {
    modalEl.addEventListener('click', (e) => {
      // 仅当点击到遮罩层（而非内容）时关闭
      if (e.target === modalEl) {
        closeQuality();
      }
    });
  }
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeQuality();
    }
  });
  await renderAll();
}

/**
 * 工具函数：从API获取JSON。
 */
async function fetchJson(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error('请求失败：' + url);
  return r.json();
}

/**
 * 工具函数：将保费转换为万元，并格式化显示。
 */
function toWan(x) {
  return (Number(x) || 0) / 10000;
}
function fmtWanDisplay(x) {
  const v = toWan(x);
  return v.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

/**
 * 工具函数：格式化百分比。
 */
function fmtPercent(x) {
  const v = (Number(x) || 0) * 100;
  return v.toLocaleString('zh-CN', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';
}

/**
 * 渲染所有图表：每日指标、原保与批单、交强vs商业、机构Top10、渠道Top10。
 */
async function renderAll() {
  const start = document.getElementById('startDate').value;
  const end = document.getElementById('endDate').value;
  if (!start || !end) return;

  const daily = await fetchJson(`/api/daily?start=${start}&end=${end}`);
  const kpi = await fetchJson(`/api/kpi?start=${start}&end=${end}`);
  const org = await fetchJson(`/api/dim?type=org&start=${start}&end=${end}`);
  const channel = await fetchJson(`/api/dim?type=channel&start=${start}&end=${end}`);
  const risk = await fetchJson(`/api/dim?type=risk&start=${start}&end=${end}`);
  const monthly = await fetchJson(`/api/monthly?start=${start}&end=${end}`);

  renderKPI(kpi);
  renderNet(daily);
  renderOP(daily);
  renderRisk(daily);
  renderMonthly(monthly);
  renderDimTop(org, 'chartOrg');
  renderDimTop(channel, 'chartChannel');
}

/**
 * 渲染KPI卡片：净保费、原保保费、批单净额、总件数、商险/交强占比。
 */
function renderKPI(kpi) {
  const setText = (id, text) => { const el = document.getElementById(id); if (el) el.textContent = text; };
  setText('kpi_net', fmtWanDisplay(kpi['净保费']) + ' 万');
  setText('kpi_orig', fmtWanDisplay(kpi['原保保费']) + ' 万');
  setText('kpi_endo', fmtWanDisplay(kpi['批单保费净额']) + ' 万');
  setText('kpi_total_cnt', (kpi['总件数'] || 0).toLocaleString('zh-CN'));
  setText('kpi_comm_ratio', fmtPercent(kpi['商业占比']));
  setText('kpi_mtpl_ratio', fmtPercent(kpi['交强占比']));
}

/**
 * 渲染净保费趋势（折线图）。
 */
function renderNet(daily) {
  const el = document.getElementById('chartNet');
  const chart = echarts.init(el, null, { renderer: 'canvas' });
  const dates = daily.map(x => x['日期']);
  const net = daily.map(x => toWan(x['净保费']));

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const lines = params.map(p => `${p.seriesName}: ${fmtWanDisplay(p.value)} 万元`);
        return `${params[0].axisValue}<br/>${lines.join('<br/>')}`;
      }
    },
    xAxis: { type: 'category', data: dates, axisLine: { lineStyle: { color: '#333' } }, axisLabel: { color: '#bbb' } },
    yAxis: { type: 'value', name: '单位：万元', nameTextStyle: { color: '#888' }, nameGap: 24, axisLine: { lineStyle: { color: '#333' } }, splitLine: { lineStyle: { color: '#111' } }, axisLabel: { color: '#bbb' } },
    series: [{
      name: '净保费', type: 'line', smooth: true,
      data: net,
      lineStyle: { color: '#00c2ff', width: 3 },
      areaStyle: { color: 'rgba(0, 194, 255, 0.12)' }
    }]
  });
}

/**
 * 渲染原保与批单保费（堆叠柱状）。
 */
function renderOP(daily) {
  const el = document.getElementById('chartOP');
  const chart = echarts.init(el);
  const dates = daily.map(x => x['日期']);
  const orig = daily.map(x => toWan(x['原保保费']));
  const endo = daily.map(x => toWan(x['批单保费净额']));

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const lines = params.map(p => `${p.seriesName}: ${fmtWanDisplay(p.value)} 万元`);
        return `${params[0].axisValue}<br/>${lines.join('<br/>')}`;
      }
    },
    legend: { textStyle: { color: '#bbb' } },
    xAxis: { type: 'category', data: dates, axisLabel: { color: '#bbb' }, axisLine: { lineStyle: { color: '#333' } } },
    yAxis: { type: 'value', name: '单位：万元', nameTextStyle: { color: '#888' }, nameGap: 24, axisLabel: { color: '#bbb' }, splitLine: { lineStyle: { color: '#111' } }, axisLine: { lineStyle: { color: '#333' } } },
    series: [
      { name: '原保保费', type: 'bar', stack: 'total', data: orig, itemStyle: { color: '#27AE60' } },
      { name: '批单保费净额', type: 'bar', stack: 'total', data: endo, itemStyle: { color: '#E67E22' } },
    ]
  });
}

/**
 * 渲染交强/商业（双折线）。
 */
function renderRisk(daily) {
  const el = document.getElementById('chartRisk');
  const chart = echarts.init(el);
  const dates = daily.map(x => x['日期']);
  const mtpl = daily.map(x => toWan(x['交强保费']));
  const comp = daily.map(x => toWan(x['商业保费']));

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const lines = params.map(p => `${p.seriesName}: ${fmtWanDisplay(p.value)} 万元`);
        return `${params[0].axisValue}<br/>${lines.join('<br/>')}`;
      }
    },
    legend: { textStyle: { color: '#bbb' } },
    xAxis: { type: 'category', data: dates, axisLabel: { color: '#bbb' }, axisLine: { lineStyle: { color: '#333' } } },
    yAxis: { type: 'value', name: '单位：万元', nameTextStyle: { color: '#888' }, nameGap: 24, axisLabel: { color: '#bbb' }, splitLine: { lineStyle: { color: '#111' } }, axisLine: { lineStyle: { color: '#333' } } },
    series: [
      { name: '交强保费', type: 'line', smooth: true, data: mtpl, lineStyle: { color: '#8E44AD', width: 3 } },
      { name: '商业保费', type: 'line', smooth: true, data: comp, lineStyle: { color: '#3498DB', width: 3 } },
    ]
  });
}

/**
 * 渲染维度Top10（条形图）：机构或渠道。
 */
function renderDimTop(records, elId) {
  const el = document.getElementById(elId);
  const chart = echarts.init(el);
  // 汇总同维度的保费之和
  const sumMap = new Map();
  for (const r of records) {
    const dim = r['维度'];
    const val = toWan(r['保费']);
    sumMap.set(dim, (sumMap.get(dim) || 0) + val);
  }
  const arr = Array.from(sumMap.entries()).map(([k, v]) => ({ name: k || '(空)', value: v }));
  arr.sort((a, b) => b.value - a.value);
  const top = arr.slice(0, 10);
  const names = top.map(x => x.name);
  const values = top.map(x => x.value);

  chart.setOption({
    backgroundColor: 'transparent',
    grid: { left: 120, right: 20 },
    tooltip: {
      trigger: 'axis', axisPointer: { type: 'shadow' },
      formatter: (params) => {
        const p = params[0];
        return `${p.name}<br/>保费：${fmtWanDisplay(p.value)} 万元`;
      }
    },
    xAxis: { type: 'value', name: '单位：万元', nameTextStyle: { color: '#888' }, nameGap: 24, axisLabel: { color: '#bbb' }, splitLine: { lineStyle: { color: '#111' } }, axisLine: { lineStyle: { color: '#333' } } },
    yAxis: { type: 'category', data: names, axisLabel: { color: '#bbb' }, axisLine: { lineStyle: { color: '#333' } } },
    series: [{
      type: 'bar', data: values,
      itemStyle: { color: '#00c2ff' },
      barWidth: 18,
      label: { show: true, position: 'right', color: '#bbb', formatter: (p) => fmtWanDisplay(p.value) + ' 万元' }
    }]
  });
}

/**
 * 渲染月度净保费对比（柱状）。
 */
function renderMonthly(records) {
  const el = document.getElementById('chartMonthly');
  const chart = echarts.init(el);
  const months = records.map(x => x['月份']);
  const values = records.map(x => toWan(x['签单保费']));
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis', axisPointer: { type: 'shadow' },
      formatter: (params) => `${params[0].axisValue}<br/>净保费：${fmtWanDisplay(params[0].value)} 万元`
    },
    xAxis: { type: 'category', data: months, axisLabel: { color: '#bbb' }, axisLine: { lineStyle: { color: '#333' } } },
    yAxis: { type: 'value', name: '单位：万元', nameTextStyle: { color: '#888' }, nameGap: 24, axisLabel: { color: '#bbb' }, splitLine: { lineStyle: { color: '#111' } }, axisLine: { lineStyle: { color: '#333' } } },
    series: [{ type: 'bar', data: values, itemStyle: { color: '#27AE60' }, barWidth: 20, label: { show: true, position: 'top', color: '#bbb', formatter: (p) => fmtWanDisplay(p.value) } }]
  });
}

/**
 * 打开质量检查弹窗：加载负保费与重复保单数据并渲染表格。
 */
async function openQuality() {
  const start = document.getElementById('startDate').value;
  const end = document.getElementById('endDate').value;
  const q = await fetchJson(`/api/quality?start=${start}&end=${end}`);
  renderTable('tblNegative', q.negative, ['报告日期','所属机构','渠道名称','保单号','批单号','签单保费','险种名称']);
  renderTable('tblDup', q.duplicates, ['报告日期','所属机构','渠道名称','保单号','批单号','签单保费','险种名称']);
  document.getElementById('dupCount').textContent = (q.duplicate_count || 0).toString();
  document.getElementById('qualityModal').hidden = false;
}

/**
 * 关闭质量检查弹窗。
 */
function closeQuality() {
  document.getElementById('qualityModal').hidden = true;
}

/**
 * 渲染简单表格。
 */
function renderTable(id, rows, cols) {
  const el = document.getElementById(id);
  if (!el) return;
  const thead = '<thead><tr>' + cols.map(c => `<th>${c}</th>`).join('') + '</tr></thead>';
  const tbody = '<tbody>' + rows.map(r => {
    return '<tr>' + cols.map(c => {
      let v = r[c];
      if (c === '签单保费') v = fmtWanDisplay(v) + ' 万元';
      return `<td>${v ?? ''}</td>`;
    }).join('') + '</tr>';
  }).join('') + '</tbody>';
  el.innerHTML = thead + tbody;
}

// 启动
init().catch(err => {
  console.error(err);
  const metaEl = document.getElementById('meta');
  metaEl.textContent = '初始化失败：' + err.message;
});