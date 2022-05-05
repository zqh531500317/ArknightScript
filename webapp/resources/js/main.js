console.info("init start")
Neutralino.init();
Neutralino.events.on('windowClose', (e) => {
        Neutralino.os.showMessageBox('Confirm',
            'Are you sure you want to quit?',
            'YES_NO', 'QUESTION').then((button) => {
            if (button === 'YES') {
                axios({
                    method: 'get',
                    url: base_url + "/shutdown"
                })
                Neutralino.app.exit();
            }
        });
    }
);
Neutralino.os.execCommand('start_flask.py', {background: true})
console.info("init completed")