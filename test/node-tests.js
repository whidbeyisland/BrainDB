// Mocha tests

var expect = require('chai').expect;
var index = require('../index');

describe('Web Server', function() {
    it('exists', function() {
        var result = index.testFunc(3);

        expect(result).to.equal(4);
    });
});