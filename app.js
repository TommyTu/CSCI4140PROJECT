// "E:\Program Files\MongoDB\Server\3.6\bin\mongod.exe"
// net start MongoDB
// net stop MongoDB

const express = require('express'),
    app = express(),
    mongoose = require('mongoose'),
    session = require('express-session'),
    bodyParser = require('body-parser'),
    // cookieParser = require('cookie-parser'),
    flash = require('connect-flash');
    
const indexRoute = require('./routes/index'),
    commentRoute = require('./routes/comment'),
    searchRoute = require('./routes/search'),
    protectedRoute = require('./routes/protected');

process.env.TZ = 'Hongkong';

const dbPath = 'mongodb://localhost/csci4140_db';
mongoose.connect(dbPath);
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connnection error:'));

app.set('view engine', 'ejs');
app.use("/",express.static(__dirname + "/public"));

app.use(flash());

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
// app.use(cookieParser());
app.use(session({
    secret: 'csci4140',
    resave: false,
    saveUninitialized: false
}));

app.use("/", indexRoute);
app.use("/comment", commentRoute);
app.use("/search", searchRoute);
app.use("/protected", protectedRoute);

app.use(function(req, res, next){
  res.redirect('/');
});

app.listen(3000, () => {
    console.log('CUTE server has started');
});