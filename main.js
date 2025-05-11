const { app, BrowserWindow } = require('electron');
const { spawn } = require("child_process");
const path = require('path');
const kill = require('tree-kill');

let mainWindow;
let flaskProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    icon: path.join(__dirname, 'static', 'favicon.ico'),
  });

  mainWindow.setMenuBarVisibility(false);

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  const tryLoad = () => {
    fetch("http://localhost:5000")
      .then(() => mainWindow.loadURL("http://localhost:5000"))
      .catch(() => setTimeout(tryLoad, 500));
  };

  tryLoad();
}

app.on('ready', () => {
  const scriptPath = path.join(__dirname, 'dist', 'app', 'app.exe');
  
  flaskProcess = spawn(scriptPath, {
    cwd: path.dirname(scriptPath),
    windowsHide: true,
    stdio: "ignore"
  });

  createWindow();
});

app.on('window-all-closed', () => {
  if (flaskProcess && flaskProcess.pid) {
    kill(flaskProcess.pid);
  }
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
