/* eslint global-require: off, no-console: off, promise/always-return: off */

/**
 * This module executes inside of electron's main process. You can start
 * electron renderer process from here and communicate with the other processes
 * through IPC.
 *
 * When running `npm run build` or `npm run build:main`, this file is compiled to
 * `./src/main.js` using webpack. This gives us some performance wins.
 */
import path from 'path';
import { app, BrowserWindow, shell, ipcMain } from 'electron';
import { autoUpdater } from 'electron-updater';
import log from 'electron-log';
import MenuBuilder from './menu';
import { resolveHtmlPath } from './util';

import { StartScreenController } from './Controller/StartScreenController';
import { kill } from 'process';


const isDebug =
  process.env.NODE_ENV === 'development' || process.env.DEBUG_PROD === 'true';

class AppUpdater {
  constructor() {
    log.transports.file.level = 'info';
    autoUpdater.logger = log;
    autoUpdater.checkForUpdatesAndNotify();
  }
}

//BACKEND INIT

class mainController {
  startScreenController: StartScreenController

      constructor() {
          this.startScreenController = new StartScreenController();
      }

}

var main = new mainController();


//-------

let mainWindow: BrowserWindow | null = null;

//IPC CONNECTIONS

ipcMain.on('ipc-example', async (event, arg) => {
  const msgTemplate = (pingPong: string) => `IPC test: ${pingPong}`;
  console.log(msgTemplate(arg));
  event.reply('ipc-example', msgTemplate('pong'));
});

ipcMain.on('start', async (event, arg) => {
  if (arg == ""){
    event.reply('start', console.log(main.startScreenController.checkFlaskStatus()));
  }
  else{
    event.reply('start', console.log("Undefined ipc request from start screen"));
  }

});








//--------------------

if (process.env.NODE_ENV === 'production') {
  const sourceMapSupport = require('source-map-support');
  sourceMapSupport.install();
}


if (isDebug) {
  require('electron-debug')();
}

const installExtensions = async () => {
  const installer = require('electron-devtools-installer');
  const forceDownload = !!process.env.UPGRADE_EXTENSIONS;
  const extensions = ['REACT_DEVELOPER_TOOLS'];

  return installer
    .default(
      extensions.map((name) => installer[name]),
      forceDownload,
    )
    .catch(console.log);
};

const createWindow = async () => {
  
  //backend flask
  if (app.isPackaged == false){ // fork process directly from main.py when not packaged (compiled into exe)
    
    console.log(`Initializing flask connection to backend: \n`); // when error
    var python = require('child_process').spawn('py', ['./Python_Backend/main.py']);
    python.stdout.on('data', function (data: { toString: (arg0: string) => any; }) {
      console.log("data: ", data.toString('utf8'));
      console.log("directory name is: " + __dirname);
    });
    python.stderr.on('data', (data: any) => {
      console.log(`stderr: ${data}`); // when error
    });
  }
  else{ //will fork process from python portable exe
      //var pythonExe = require('child_process').spawn("D:/Programming/MetRocketry/Groundstation-GUI_Electron/release/build/win-unpacked/main.exe");
      //note that '../../../../' is needed as the actual directory to the root project files is embedded deeper in __dirname
      var pythonExe = require('child_process').spawn( path.join(__dirname, '../../../../') + "main.exe");

  }
  //---------------------------------


  if (isDebug) {
    await installExtensions();
  }

  const RESOURCES_PATH = app.isPackaged
    ? path.join(process.resourcesPath, 'assets')
    : path.join(__dirname, '../../assets');

  const getAssetPath = (...paths: string[]): string => {
    return path.join(RESOURCES_PATH, ...paths);
  };

  // WINDOW CONFIG
  mainWindow = new BrowserWindow({
    show: false,
    width: 1920,
    height: 1080,
    icon: getAssetPath('icon.png'),
    webPreferences: {
      preload: app.isPackaged
        ? path.join(__dirname, 'preload.js')
        : path.join(__dirname, '../../.erb/dll/preload.js'), 
    },
    
  });

  //----------------------------------------------------

  //load initial page
  mainWindow.loadURL(resolveHtmlPath('index.html'));

  mainWindow.on('ready-to-show', () => {
    if (!mainWindow) {
      throw new Error('"mainWindow" is not defined');
    }
    if (process.env.START_MINIMIZED) {
      mainWindow.minimize();
    } else {
      mainWindow.show();
    }
  });

  mainWindow.on('closed', () => {
    app.quit(); //note that this force exits the app, will kill child flask server automatically
    //kill(pythonExe.pid, "SIGKILL"); //kill the child flask server
    mainWindow = null;
  });

  const menuBuilder = new MenuBuilder(mainWindow);
  menuBuilder.buildMenu();

  // Open urls in the user's browser
  mainWindow.webContents.setWindowOpenHandler((edata) => {
    shell.openExternal(edata.url);
    return { action: 'deny' };
  });

  // Remove this if your app does not use auto updates
  // eslint-disable-next-line
  new AppUpdater();
};

/**
 * Add event listeners...
 */

app.on('window-all-closed', () => {
  // Respect the OSX convention of having the application in memory even
  // after all windows have been closed
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app
  .whenReady()
  .then(() => {
    createWindow();
    app.on('activate', () => {
      // On macOS it's common to re-create a window in the app when the
      // dock icon is clicked and there are no other windows open.
      if (mainWindow === null) createWindow();
    });
  })
  .catch(console.log);
