// Mocha tests

var expect = require('chai').expect;
var index = require('../index');

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
});

describe('Loading Screen', function() {
    it('generates a string for the loading screen', function() {
        var result = index.generateHTMLString('html/htmlsection-loading.html');
        expect(result).to.be.a('string');
    });
});

describe('Card Generation', function() {

});

describe('Local Storage, Cards', function() {

});

describe('Remote Storage, Cards', function() {

});