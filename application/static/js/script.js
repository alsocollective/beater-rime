var app = {
	init: function() {
		app.getdata.init();
		app.submit.init();
	},
	dataLoaded: function() {
		console.log("dataLoaded")
		$("#user").change(app.user.checkIfWorking);
		app.user.checkForCookie();
	},
	getdata: {
		init: function() {
			app.getdata.user(app.user.retrivedData);
			app.getdata.projects(app.project.retrivedData);
		},
		user: function(returnfunction) {
			$.ajax("/api/people").done(returnfunction).fail(app.getdata.error).always(app.getdata.doneLoading);
		},
		projects: function(returnfunction) {
			$.ajax("/api/projects").done(returnfunction).fail(app.getdata.error).always(app.getdata.doneLoading);
		},
		loadingcount: 0,
		doneLoading: function() {
			++app.getdata.loadingcount;
			if (app.getdata.loadingcount == 2) {
				app.dataLoaded();
			}
		},
		error: function() {
			console.log("error loading data");
		}
	},
	user: {
		data: [],
		retrivedData: function(data) {
			console.log(data)
			app.user.data = data;
		},
		checkForCookie: function() {
			var name = $.cookie('name');
			$("#user").val(name);
			app.user.checkIfWorking(name);
		},
		checkIfWorking: function(name) {
			//check if the name is passed to it
			var name = name;
			if (this.value || this.value == 0) {
				name = this.value;
			}

			var project = app.project.byUser(name);
			if (project) {
				$("#project").val(project);
				console.log("user is working");
				app.setUpWorking.init();
			} else {
				app.setUpWorking.cleanup();
			}


		},
		currentUserNumber: function() {
			var a = 0,
				max = app.user.data.length,
				selected = $("#user").val();
			for (a = 0; a < max; ++a) {
				if (app.user.data[a].pk == selected) {
					return a;
				}
			}
		}
	},
	project: {
		data: {},
		retrivedData: function(data) {
			app.project.data = data;
		},
		byUser: function(username) {
			var a = 0,
				max = app.user.data.length;
			for (a = 0; a < max; ++a) {
				if (app.user.data[a].pk == parseInt(username)) {
					if (app.user.data[a].project) {
						return app.user.data[a].pk
					};
					return false
				}
			}
			return "";
		}
	},
	setUpWorking: {
		init: function() {
			console.log("setup working");
			app.submit.type.stop();
			app.timer.init();
			$("#wrapper").addClass("working");
		},
		cleanup: function() {
			console.log("cleanup working");
			app.submit.type.start();
			app.timer.stop();
			$("#wrapper").removeClass("working");
		}
	},
	submit: {
		init: function() {
			$("#start").click(app.submit.start);
		},
		start: function(event) {
			$.cookie('name', $("#user").val());
			$("#datetime").val(Date.parse(new Date) / 1000);
		},
		type: {
			stop: function() {
				$("form").attr("action", "/api/stoptimmer")
			},
			start: function() {
				$("form").attr("action", "/api/starttimmer")
			}
		}
	},
	timer: {
		time: {
			startDate: null,
			start: null,
			dateold: null
		},
		init: function() {
			var user = app.user.currentUserNumber(),
				datenow = new Date(),
				dateold = new Date(app.user.data[user].start * 1000),
				// time = app.user.data[user][3].split(":"),
				// date = app.user.data[user][2].split("/"),
				minutesworked = 0;
			// app.timer.time.startDate = date;
			// app.timer.time.start = time;
			// dateold.setHours(time[0], time[1], time[2]);
			// dateold.setMonth(date[1], date[0]);
			app.timer.time.dateold = dateold;

			minutesworked = Math.ceil(Math.abs(datenow.getTime() - dateold.getTime()) / (1000));
			console.log("minutes worked " + minutesworked);
			app.timer.ticker = setInterval(app.timer.tick, 1000);
		},
		ticker: null,
		tick: function() {
			console.log("tick");
			var datenow = new Date(),
				dateold = app.timer.time.dateold,
				time = app.timer.toTimeNumber(Math.abs(datenow.getTime() - dateold.getTime()) / (60000));
			app.timer.renderTime(time, app.timer.toTimeDate(dateold), app.timer.toTimeDate(datenow));
		},
		toTimeDate: function(date) {
			return date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
		},
		toTimeNumber: function(ammount) {
			var flat = Math.floor(ammount),
				small = Math.floor(((Math.ceil(ammount * 100) / 100.0) - flat) * 60)
			return flat + ":" + small;
		},
		renderTime: function(time, start, current) {
			$("#currenttime").html(current);
			$("#starttime").html(start);
			$("#worked").html(time);
		},
		stop: function() {
			window.clearInterval(app.timer.ticker);
		}
	}
}