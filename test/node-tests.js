// Mocha tests

var chai = require('chai');
var expect = require('chai').expect;
var chaiHttp = require('chai-http');
var index = require('../index');
var server = index.server;
chai.use(chaiHttp);

describe('Signup', function() {
    it('generates a string for the signup page', function() {
        var result = index.generateHTMLString('html/htmlsection-signup.html');
        expect(result).to.be.a('string');
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

    it('throws an error when the user enters a blank login', (done) => {
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

    it('throws an error when the user does not enter a username', (done) => {
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

    it('throws an error when the user does not enter a username', (done) => {
        let credentials = {
            username: 'password',
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
});

describe('Loading Screen', function() {
    it('generates a string for the loading screen', function() {
        var result = index.generateHTMLString('html/htmlsection-loading.html');
        expect(result).to.be.a('string');
    });
});

/*
describe('Card Generation', function() {

});

describe('Local Storage, Cards', function() {

});

describe('Remote Storage, Cards', function() {

});
*/