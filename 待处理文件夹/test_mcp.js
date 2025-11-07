#!/usr/bin/env node

const { spawn } = require('child_process');

// Test filesystem MCP server
console.log('Testing filesystem MCP server...');
const fsServer = spawn('node', ['node_modules/@modelcontextprotocol/server-filesystem/dist/index.js'], {
  stdio: 'pipe'
});

fsServer.stdout.on('data', (data) => {
  console.log(`Filesystem MCP: ${data}`);
});

fsServer.stderr.on('data', (data) => {
  console.error(`Filesystem MCP Error: ${data}`);
});

setTimeout(() => {
  fsServer.kill();
  console.log('Filesystem MCP test completed.');
}, 3000);