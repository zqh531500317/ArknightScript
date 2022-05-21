import {neu_version} from "@/config";

export const checkupdate = async () => {
    try {
        let url = "http://example.com/updater_test/update_manifest.json";
        let manifest = await window.Neutralino.updater.checkForUpdates(url);
        if (manifest.version !== neu_version) {
            await window.Neutralino.updater.install();
            await window.Neutralino.app.restartProcess();
        }
    } catch (err) {
        // Handle errors
    }
}
