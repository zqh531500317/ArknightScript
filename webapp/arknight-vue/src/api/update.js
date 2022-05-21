import {neu_version} from "@/config";
import {myMessage} from "@/util/utils";

export const checkupdate = async () => {
    try {
        let url = 'https://raw.githubusercontent.com/zqh531500317/arknight-script/master/webapp/%20update_manifest.json'
        let manifest = await window.Neutralino.updater.checkForUpdates(url);
        if (manifest.version !== neu_version) {
            myMessage("有新的更新,当前版本:" + neu_version + "最新版本:" + manifest.version)
            await window.Neutralino.updater.install();
            await window.Neutralino.app.restartProcess();
        }
    } catch (err) {
        // Handle errors
    }
}
