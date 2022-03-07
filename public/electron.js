const electron = require('electron');
const path = require('path');
const url = require('url');

const { app } = electron;
const { BrowserWindow } = electron;

const { ipcMain } = require('electron');

let mainWindow;

function createWindow() {
	const startUrl = process.env.DEV
		? 'http://localhost:3000'
		: url.format({
			pathname: path.join(__dirname, '/../build/index.html'),
			protocol: 'file:',
			slashes: true,
		});
	mainWindow = new BrowserWindow({
		width: 1920,
		height: 1280,
		webPreferences: {
			nodeIntegration: true,
			contextIsolation: false,
		},
	});

	mainWindow.loadURL(startUrl);
	process.env.DEV && mainWindow.webContents.openDevTools();

	mainWindow.on('closed', function () {
		mainWindow = null;
	});
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit();
	}
});

app.on('activate', () => {
	if (mainWindow === null) {
		createWindow();
	}
});

let cache = {
	url: undefined,
	keywords: undefined,
	cuts: undefined,
	file: undefined,
};


let hiddenWindow;

ipcMain.on('toElectron : start background', (event, args) => {
	const backgroundFileUrl = url.format({
		pathname: path.join(__dirname, `../background_tasks/background.html`),
		protocol: 'file:',
		slashes: true,
	});
	hiddenWindow = new BrowserWindow({
		show: false,
		webPreferences: {
			nodeIntegration: true,
		},
	});
	hiddenWindow.loadURL(backgroundFileUrl);

	hiddenWindow.webContents.openDevTools();

	hiddenWindow.on('closed', () => {
		hiddenWindow = null;
	});
});
ipcMain.on('toElectron : background opening', (event, args) => {

	mainWindow.webContents.send('toApp : background opening', 'background open');
});



ipcMain.on('toElectron : process call [stream analysis]', (event, args) => {
	cache.url = args.url;
	hiddenWindow.webContents.send('toBack : process call [stream analysis]', {
		url: cache.url,
	});
});
ipcMain.on('toElectron : process result [stream analysis]', (event, args) => {
	mainWindow.webContents.send('toApp : process result [stream analysis]', args.message);
});



ipcMain.on('toElectron : process call [keywords search]', (event, args) => {
	cache.keywords = args.keywords;
	hiddenWindow.webContents.send('toBack : process call [keywords search]', {
		url: cache.url,
		keywords: cache.keywords,
	});
});
ipcMain.on('toElectron : process result [keywords search]', (event, args) => {
	mainWindow.webContents.send('toApp : process result [keywords search]', args.message);
});



ipcMain.on('toElectron : process call [cuts output]', (event, args) => {
	cache.cuts = args.cuts;
	cache.file = args.file;
	hiddenWindow.webContents.send('toBack : process call [cuts output]', {
		cuts: cache.cuts,
		file: cache.file,
	});
});
ipcMain.on('toElectron : process result [cuts output]', (event, args) => {
	mainWindow.webContents.send('toApp : process result [cuts output]', args.message);
});

