const path = require('path');
const pathToStatic = path.resolve(__dirname, '../static');

module.exports = function (grunt) {
    const sass = require('sass');
    grunt.loadNpmTasks('grunt-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-concurrent');

    grunt.registerTask('default', ['concurrent:watchall']);

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        // SASS Task
        sass: {
            main: {
                options: {
                    sourceMap: true,
                    outputStyle: 'compressed',
                    implementation: sass,
                },
                files: {
                    [`${pathToStatic}/styles/styles.css`]: `${pathToStatic}/styles/scss/main.scss`,
                },
            },
        },

        // Uglify
        uglify: {
            main: {
                options: {
                    sourceMap: false,
                    compress: true,
                    mangle: false,
                },
                files: {
                    [`${pathToStatic}/js/scripts.min.js`]: [`${pathToStatic}/js/scripts/**/*.js`],
                },
            },
            vendor: {
                options: {
                    sourceMap: false,
                    compress: true,
                    mangle: false,
                },
                files: {
                    [`${pathToStatic}/js/scripts-vendor.min.js`]: [
                        './node_modules/bootstrap/dist/js/bootstrap.min.js',
                        './node_modules/lightgallery/lightgallery.min.js',
                    ],
                },
            },
        },

        // Watch Task
        watch: {
            scss: {
                files: [`${pathToStatic}/styles/scss/**/*.scss`],
                tasks: ['sass:main'],
                options: {
                    spawn: false,
                },
            },
            js: {
                files: [`${pathToStatic}/js/scripts/**/*.js`],
                tasks: ['uglify:main'],
                options: {
                    spawn: false,
                },
            },
        },

        // Concurrent Task
        concurrent: {
            options: {
                logConcurrentOutput: true,
                limit: 10,
            },
            watchall: {
                tasks: ['watch:scss', 'watch:js'],
            },
        },
    });

    // Register Additional Tasks
    grunt.registerTask('vendors', ['uglify:vendor']);
};
