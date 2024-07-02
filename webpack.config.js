//wepback.config.js
const path = require('path');
const webpack = require('webpack');
const packageJson = require('./node_modules/socket.io-client/package.json');


module.exports = {
    entry: ['./lib/client.js', './lib/index.js', './lib/namespace.js', './lib/parent-namespace.js', './lib/socket.js'],
    output: {
        filename: 'libs.js',
        path: path.resolve(__dirname, 'static'),
    },
    mode: 'development',
    resolve: {
        extensions: ['.js', '.json'],
        modules: [path.resolve(__dirname, 'node_modules'), 'node_modules'],
        fallback: {
            "url": require.resolve("url/"),
            "http": require.resolve("stream-http"),
            "path": require.resolve("path-browserify"),
            "zlib": require.resolve("browserify-zlib"),
            "timers": require.resolve("timers-browserify"),
            "crypto": require.resolve("crypto-browserify"),
            "stream": require.resolve("stream-browserify"),
            "assert": require.resolve("assert/"),
            "util": require.resolve("util/"),
            "vm": require.resolve("vm-browserify"),   
            "buffer": require.resolve("buffer"),
            "process": require.resolve("process"),
            "net": false,
            "tls": false,
            "fs": false
        }
    },
    plugins: [
        new webpack.ProvidePlugin({
            Buffer: ['buffer', 'Buffer'],
        }),
        new webpack.DefinePlugin({
            'SOCKET_IO_CLIENT_VERSION': JSON.stringify(packageJson.version)
        }),
        new webpack.ProvidePlugin({
            process: 'process/browser', 
            util:    'util',
            Buffer: ['buffer', 'Buffer'],
        }),
        new webpack.ContextReplacementPlugin(
            /(.+)?/,
            path.resolve(__dirname, 'src'),),
            new webpack.ProvidePlugin({
                util: 'util', // Provide a polyfill for 'util'
            })
    ],
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            }
        ]
    },

    externals: {
        util: 'util', // Exclude 'util' from bundling
        assert: 'assert', // Exclude 'assert' from bundling
        // Add other modules as needed
    }
};