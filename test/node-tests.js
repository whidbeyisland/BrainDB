// Mocha tests

var fs = require('fs');
var chai = require('chai');
var expect = require('chai').expect;
var chaiHttp = require('chai-http');
var index = require('../index');
var server = index.server;
chai.use(chaiHttp);

var default_text = '';
fs.readFile('../default-card-source.txt', 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      return;
    }
    default_text = data;
});

describe('Signup', function() {
    it('generates a string for the signup page', function() {
        var result = index.generateHTMLString('html/htmlsection-signup.html');
        expect(result).to.be.a('string');
    });

    it('throws an error when the user does not enter credentials on signup', (done) => {
        let credentials = {
            username: '',
            password: ''
        }
        chai.request(server)
            .post('/signup')
            .send(credentials)
            .end((err, res) => {
                expect(res).to.have.status(404);
            done();
        });
    });

    it('throws an error when the user does not enter a username on signup', (done) => {
        let credentials = {
            username: '',
            password: 'password'
        }
        chai.request(server)
            .post('/signup')
            .send(credentials)
            .end((err, res) => {
                expect(res).to.have.status(404);
            done();
        });
    });

    it('throws an error when the user does not enter a password on signup', (done) => {
        let credentials = {
            username: 'username',
            password: ''
        }
        chai.request(server)
            .post('/signup')
            .send(credentials)
            .end((err, res) => {
                expect(res).to.have.status(404);
            done();
        });
    });
});

describe('Confirmation', function() {
    it('generates a string for the code confirmation screen', function() {
        var result = index.generateHTMLString('html/htmlsection-confirm.html');
        expect(result).to.be.a('string');
    });
});

describe('Login', function() {
    it('generates a string for the login page', function() {
        var result = index.generateHTMLString('html/htmlsection-login.html');
        expect(result).to.be.a('string');
    });

    it('throws an error when the user does not enter credentials on login', (done) => {
        let credentials = {
            username: '',
            password: ''
        }
        chai.request(server)
            .post('/login')
            .send(credentials)
            .end((err, res) => {
                expect(res).to.have.status(404);
            done();
        });
    });

    it('throws an error when the user does not enter a username on login', (done) => {
        let credentials = {
            username: '',
            password: 'password'
        }
        chai.request(server)
            .post('/login')
            .send(credentials)
            .end((err, res) => {
                expect(res).to.have.status(404);
            done();
        });
    });

    it('throws an error when the user does not enter a password on login', (done) => {
        let credentials = {
            username: 'FakeUserName',
            password: ''
        }
        chai.request(server)
            .post('/login')
            .send(credentials)
            .end((err, res) => {
                expect(res).to.have.status(404);
            done();
        });
    });

    it('throws an error when the user enters an incorrect username or password', (done) => {
        let credentials = {
            username: 'FakeUserName',
            password: 'password'
        }
        chai.request(server)
            .post('/login')
            .send(credentials)
            .end((err, res) => {
                expect(res).to.have.status(404);
            done();
        });
    });
});

describe('Loading Screen', function() {
    it('generates a string for the loading screen', function() {
        var result = index.generateHTMLString('html/htmlsection-loading.html');
        expect(result).to.be.a('string');
    });
});

describe('Card Generation', function() {
    it('throws an error when the user does not enter text or a deck name', (done) => {
        let text_deck = {
            myText: '',
            deckName: ''
        }
        chai.request(server)
            .post('/upload')
            .send(text_deck)
            .end((err, res) => {
                expect(res).to.have.status(404);
            done();
        });
    });

    it('throws an error when the user does not enter text', (done) => {
        let text_deck = {
            myText: '',
            deckName: 'Test Deck'
        }
        chai.request(server)
            .post('/upload')
            .send(text_deck)
            .end((err, res) => {
                expect(res).to.have.status(404);
            done();
        });
    });
    
    it('throws an error when the user does not enter a deck name', (done) => {
        let text_deck = {
            myText: default_text,
            deckName: ''
        }
        chai.request(server)
            .post('/upload')
            .send(text_deck)
            .end((err, res) => {
                expect(res).to.have.status(404);
            done();
        });
    });
});