const chai = require('chai');
const chaiHttp = require('chai-http');
const server = require('../app');
const should = chai.should();
const expect = chai.expect;
chai.use(chaiHttp);
const Promise = require("bluebird");
const chaiAsPromised = require("chai-as-promised");
chai.use(chaiAsPromised);
const {Builder, By, Key, until} = require('selenium-webdriver'),
    chrome = require('selenium-webdriver/chrome');
var driver;

const options = new chrome.Options();
options.addArguments(
    'headless'
);

var rgbToHex = function (rgb) {
    let hex = Number(rgb).toString(16);
    if (hex.length < 2) {
        hex = "0" + hex;
    }
    return hex;
};

describe('list view test', function() {
    this.timeout(100000);

    before(function(done){
        driver = new Builder()
            .forBrowser('chrome')
            .setChromeOptions(options)
            .build();
        driver.get('http://localhost:8000')
            .then(()=>{
                console.log("Got page");
                done();
            });
    });

    after(function(){
        driver.quit();
    });

    beforeEach(async function() {
        driver.navigate().refresh();
    });

    // it('should test load the page', async function(){
    //     let page = await driver.getPageSource();
    // });

    it('Clicking on Insert button should show alert message "Please provide the valid input" for the invalid or empty input', async function(){
        let input = await driver.findElement(By.id("input"));
        input.sendKeys("");

        let button = await driver.findElement(By.id("button"));
        await button.click();


        let alertText = await driver.switchTo().alert().getText();
        await driver.switchTo().alert().dismiss();
        expect(alertText).to.equal('Please provide the valid input');

        let list = await driver.findElements(By.tagName("li"));
        expect(list.length).to.equal(0);

        input.sendKeys(" ");

        await button.click();

        let alertText1 = await driver.switchTo().alert().getText();
        await driver.switchTo().alert().dismiss();
        expect(alertText1).to.equal('Please provide the valid input');

        list = await driver.findElements(By.tagName("li"));
        expect(list.length).to.equal(0);

        driver.takeScreenshot().then(
            function(image, err) {
                require('fs').writeFile('invalid-input.png', image, 'base64', function(err) {});
            }
        );

    });

    it('Clicking on Insert button should add the valid input to the list', async function(){
        let input = await driver.findElement(By.id("input"));
        input.sendKeys("USA");

        let button = await driver.findElement(By.id("button"));
        button.click();

        let list = await driver.findElements(By.tagName("li"));
        expect(list.length).to.equal(1);

        driver.takeScreenshot().then(
            function(image, err) {
                require('fs').writeFile('valid-input.png', image, 'base64', function(err) {});
            }
        );

    });

    it('After inserting the value successfully should reset the input', async function(){
        let input = await driver.findElement(By.id("input"));
        input.sendKeys("USA");

        let button = await driver.findElement(By.id("button"));
        button.click();

        let list = await driver.findElements(By.tagName("li"));
        expect(list.length).to.equal(1);
        let val = await input.getAttribute('value');

        expect(val).to.equal('');

        driver.takeScreenshot().then(
            function(image, err) {
                require('fs').writeFile('valid-input.png', image, 'base64', function(err) {});
            }
        );

    });

    it('Font color for every third elements (3, 6 and 9 etc) in the list should be red color', async function(){

        let input = await driver.findElement(By.id("input"));
        let button = await driver.findElement(By.id("button"));
        input.clear();
        input.sendKeys("India");
        button.click();
        input.clear();
        input.sendKeys("France");
        button.click();
        input.clear();
        input.sendKeys("Spain");
        button.click();
        input.clear();

        let list = await driver.findElements(By.tagName("li"));
        let value = await list[2].getCssValue('color');
        value = value.substring(5, value.length-1)
            .replace(/ /g, '')
            .split(',');

        value.pop();

        driver.takeScreenshot().then(
            function(image, err) {
                require('fs').writeFile('third-item-red.png', image, 'base64', function(err) {});
            }
        );
        let checkValue = value.reduce( (prev, curr) => prev + rgbToHex(curr), "#");
        expect(checkValue).to.equal('#ff0000');

    });

    it('Font color for other than every third elements (3, 6 and 9 etc) in the list should be black color', async function(){
        let input = await driver.findElement(By.id("input"));
        let button = await driver.findElement(By.id("button"));
        input.clear();
        input.sendKeys("India");
        button.click();
        input.clear();
        input.sendKeys("France");
        button.click();
        input.clear();
        input.sendKeys("Spain");
        button.click();
        input.clear();

        let list = await driver.findElements(By.tagName("li"));
        let value = await list[1].getCssValue('color');
        value = value.substring(5, value.length-1)
            .replace(/ /g, '')
            .split(',');

        value.pop();
        let checkValue = value.reduce( (prev, curr) => prev + rgbToHex(curr), "#");
        expect(checkValue).to.equal('#000000');
        driver.takeScreenshot().then(
            function(image, err) {
                require('fs').writeFile('non-third-item-block.png', image, 'base64', function(err) {});
            }
        );

    });

});
