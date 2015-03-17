module.exports = function(grunt) {
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		sass: {
			dist: {
				files: [{
					expand: true,
					cwd: 'application/static/scss',
					src: ['*.scss'],
					dest: 'application/static/css',
					ext: '.css'
				}]
			}
		},
		cssmin: {
			combine: {
				files: {
					'assets/css/style.min.css': [
						"application/static/css/normalize.min.css",
						"application/static/css/style.css",
						// "assets/css/tablet.css",
						// "assets/css/mobile.css",
						// "assets/css/videostyle.css"
					]
					// 'application/static/css/style.css': ['application/static/css/normalize.min.css', 'application/static/css/jquery.nouislider.css', 'application/static/css/slick.css', 'application/static/css/simple-style.css'],
					// 'application/static/css/tablet.min.css': 'application/static/css/tablet.css',
					// 'application/static/css/mobile.min.css': 'application/static/css/mobile.css'
				}
			}
		},
		// uglify: {
		// 	js: {
		// 		files: {
		// 			// 'application/static/js/main.min.js': [
		// 			// 	'application/static/js/lib/jquery.min.js',
		// 			// 	'application/static/js/lib/jquery.nouislider.full.min.js',
		// 			// 	'application/static/js/lib/jquery-migrate-1.2.1.min.js',
		// 			// 	'application/static/js/lib/slick.min.js',
		// 			// 	'application/static/js/lib/modernizr.js',
		// 			// 	'application/static/js/lib/waypoints.min.js',
		// 			// 	'application/static/js/main.js',
		// 			// ]
		// 		}
		// 	}
		// },
		watch: {
			css: {
				files: ['**/*.scss'],
				tasks: ['sass', 'cssmin'] //
			},
			// js: {
			// 	// files: 'application/static/js/main.js',
			// 	// tasks: ['uglify']
			// }
		}
	});
	grunt.loadNpmTasks('grunt-contrib-sass');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.registerTask('default', ['watch']);
};