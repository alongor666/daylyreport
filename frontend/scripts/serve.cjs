/**
 * 简单的静态文件服务器
 * 用于预览构建结果
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const port = 8088;  // 改用8088端口避免冲突
const publicPath = path.join(__dirname, '../dist');

const server = http.createServer((req, res) => {
  let filePath = path.join(publicPath, req.url === '/' ? '/index.html' : req.url);
  
  // 检查文件是否存在
  if (!fs.existsSync(filePath)) {
    res.writeHead(404, { 'Content-Type': 'text/html' });
    res.end('<h1>404 Not Found</h1>');
    return;
  }
  
  // 根据文件扩展名设置Content-Type
  const extname = path.extname(filePath);
  let contentType = 'text/html';
  
  switch (extname) {
    case '.js':
      contentType = 'text/javascript';
      break;
    case '.css':
      contentType = 'text/css';
      break;
    case '.json':
      contentType = 'application/json';
      break;
    case '.png':
      contentType = 'image/png';
      break;
    case '.jpg':
      contentType = 'image/jpg';
      break;
    case '.svg':
      contentType = 'image/svg+xml';
      break;
  }
  
  // 读取并发送文件
  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end('<h1>404 Not Found</h1>');
      } else {
        res.writeHead(500);
        res.end(`Server Error: ${error.code}`);
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
});

server.listen(port, () => {
  console.log(`🚀 服务器运行在 http://localhost:${port}`);
  console.log(`📁 服务目录: ${publicPath}`);
  console.log('✅ 跨操作系统主题系统已就绪！');
  console.log('');
  console.log('🎨 功能特性:');
  console.log('  • 护眼模式 - 减少蓝光，保护视力');
  console.log('  • 暗黑模式 - 适合夜间使用');
  console.log('  • 跨OS支持 - Windows/macOS/信创系统');
  console.log('  • 快捷键操作 - Alt+T/E/D');
  console.log('');
  console.log('📖 使用说明:');
  console.log(`  1. 打开浏览器访问 http://localhost:${port}`);
  console.log('  2. 点击右上角的主题切换按钮');
  console.log('  3. 体验护眼模式和暗黑模式');
  console.log('  4. 使用快捷键 Alt+T 快速切换');
});