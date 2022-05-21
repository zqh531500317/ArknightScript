const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    lintOnSave: false,
    devServer: {
        port: 8081,
        host: '0.0.0.0'
    },
    css: {
        loaderOptions: {
            postcss: {
                postcssOptions: {
                    plugins: [
                        [
                            'postcss-px-to-viewport',
                            {
                                unitToConvert: 'px',
                                viewportWidth: 1920, //视窗的宽度，对应的是我们设计稿的宽度
                                unitPrecision: 5, //制定'px’转换为视窗单位的⼩数位数（很多时候⽆法整除）
                                propList: ['*'], // 能转化为vw的属性列表
                                viewportUnit: 'vw', //指定需要转换成的视窗单位，建议使⽤
                                fontViewportUnit: 'vw', // 字体使用的视口单位
                                selectorBlackList: [], // 需要忽略的CSS选择器，不会转为视口单位，使用原有的px等单位。
                                minPixelValue: 1, //⼩于或等于'1px’不转换为视窗单位
                                mediaQuery: false, // 媒体查询里的单位是否需要转换单位
                                remUnit: 75,
                                exclude: /node_modules/,// 忽略某些文件夹下的文件或特定文件，例如 'node_modules' 下的文件
                                replace: true, //  是否直接更换属性值，而不添加备用属性
                                include: undefined, // 如果设置了include，那将只有匹配到的文件才会被转换
                                landscape: false, // 是否添加根据 landscapeWidth 生成的媒体查询条件 @media (orientation: landscape)
                                landscapeUnit: 'vw', // 横屏时使用的单位
                                landscapeWidth: 1920,// 横屏时使用的视口宽度
                                vwselectorBlackList: [
                                    //指定不需要转换的类
                                    'ignore', 'tab-bar', 'tab-bar-item', 'nav-bar', 'cart-buttom-bar', 'content'],
                                ediaQuery: false, //允许在媒体查询中转换为'px’
                            },
                        ],
                    ],
                },
            }
        }
    }
})
