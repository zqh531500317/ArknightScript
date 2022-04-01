console.info("init start")
Neutralino.init();
Neutralino.events.on('windowClose', (e) => {
        Neutralino.os.showMessageBox('Confirm',
            'Are you sure you want to quit?',
            'YES_NO', 'QUESTION').then((button) => {
            if (button === 'YES') {
                Neutralino.filesystem.readFile('../config/config.yaml').then(
                    (data) => {
                        str = JSON.stringify(data)
                        str = str.replace(/[ ]/g, "");    //去掉空格
                        str = str.replace(/(\\n)+|(\\r\\n)+/g, "");//去掉回车换行
                        patt = /pid:(\d+)/
                        pid = str.match(patt)[1]
                        Neutralino.os.execCommand('taskkill /pid ' + pid + ' -f')
                        Neutralino.app.exit();
                    }
                )

            }
        });
    }
);
Neutralino.os.execCommand('start_flask.py', {background: true})
console.info("init completed")