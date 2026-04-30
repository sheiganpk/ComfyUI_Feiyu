import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Feiyu.Settings",

    setup(app) {
        app.ui.settings.addSetting({
            id: "feiyu_api_key",
            name: "Feiyu API Key",
            type: "password",
            category: ["Feiyu", "Settings"],
            defaultValue: "请打开 https://ai.t8star.cn/register?aff=nCZC115614 注册账号并获取API Key填入此处",
        });
    }
});