var model = function(m) {
  return element(by.model(m));
};

var login = function(user) {
  element(by.model('username')).clear();
  element(by.model('username')).sendKeys(user);
  element(by.model('password')).clear();
  element(by.model('password')).sendKeys(user);
  element(by.id('loginBtn')).click();
};

var logout = function() {
  element(by.id('logoutBtn')).click();
};

describe('Authentication tests', function() {

  var tearDown = function() {
    element(by.id('logoutBtn')).click();
  };
  
  it('should have a title', function() {
    browser.get('/#/');
    expect(browser.getTitle()).toEqual('Wallfly');
  });

  it('should not let an unauthenticated user into the system', function() {
    element(by.model('username')).sendKeys("invalid");
    element(by.model('password')).sendKeys("invalid");
    element(by.id('loginBtn')).click();
    var err = element(by.id('errorTxt')).getText();
    expect(err.getText()).toEqual("Access Denied");
  });
  
  it('should let an unauthenticated user into the system', function() {
    
    element(by.model('username')).clear();
    element(by.model('username')).sendKeys("admin");
    element(by.model('password')).clear();
    element(by.model('password')).sendKeys("admin");
    element(by.id('loginBtn')).click();
    // UPDATE TO THE REAL URL
    expect(browser.getCurrentUrl()).toEqual('http://localhost:8000/#/');
    tearDown();
  });

  it('should log out an authenticated user', function() {
    element(by.model('username')).clear();
    element(by.model('username')).sendKeys("admin");
    element(by.model('password')).clear();
    element(by.model('password')).sendKeys("admin");
    element(by.id('loginBtn')).click();
    element(by.id('logoutBtn')).click();
    expect(browser.getCurrentUrl()).toEqual('http://localhost:8000/#/login');
    // logout();
  });
  
});

// issues

describe('Issue tests', function() {
  
  // create issue
  it('should create a new issue on a property', function() {
    login('admin'); 
    element.all(by.css('.propGridItemPic')).first().click();
    element(by.id('createIssueBtn')).click();

    // wait for modal to open
    var modalEl = element(by.model('issue.severity'));
    browser.wait(EC.visibilityOf(modalEl), 5000);

    element(by.model('issue.severity')).click();
    model('issue.description').sendKeys("test");
    element(by.id('issueSubmit')).click();
    var issueDesc = element.all(by.css('.issueDescription'));
    // ensure the last element in the list is the new issue
    expect(issueDesc.last().getText()).toEqual('test');

  });
  
  // resolve issue
  it('should be able to resolve an issue on a property', function() {
    var rows = element.all(by.css('.issueRow'));
    element.all(by.id('resolveBtn')).last().click();
    rows = element.all(by.css('.resolvedRow'));
  });
  
  // remove issue
  it('should be able to remove an issue', function() {
    var rows = element.all(by.css('.resolvedRow'));
    var rowCount;
    rows.count().then(function(data) {
      rowCount = data;
    }).then(function() {
      element.all(by.id('deleteBtn')).last().click();
      var updateAmount = element.all(by.css('.resolvedRow')).count();
      expect(updateAmount).toEqual(rowCount-1);
    });
  });

  it('should search for an issue', function() {
    // create an issue with the description fire
    element(by.id('createIssueBtn')).click();

    // wait for modal to open
    var modalEl = element(by.model('issue.severity'));
    browser.wait(EC.visibilityOf(modalEl), 5000);

    element(by.model('issue.severity')).click();
    model('issue.description').sendKeys("fire");
    element(by.id('issueSubmit')).click();

    // try searching for the fire issue
    element(by.id('issueSearch')).sendKeys('fire');
    
    // assert that the issue exists
    var issueDesc = element.all(by.css('.issueDescription')).first();
    expect(issueDesc.getText()).toEqual('fire');
  });
  
});

//properties
describe('Property tests', function() {

  it('should be able to create a new property', function() {
    browser.get("/#/");

    element(by.id('createBtn')).click();
    // open modal
    var createModal = element(by.model('prop.address'));
    browser.wait(EC.visibilityOf(createModal), 5000);

    // create the test property
    element(by.model('prop.address')).sendKeys("12 Test Ave, Propertyville");
    element(by.model('prop.name')).sendKeys("Test Prop");
    element(by.id('submitBtn')).click();

    element(by.model('search')).sendKeys('Test Prop');

    var p = element(by.repeater('p in properties.props'));
    var pName = p.element(by.id('propName')).getText();
    expect(pName).toEqual('Test Prop');
  });

  // this test will fail
  it('should be able to edit property information', function() {
    element(by.model('search')).sendKeys('Prop to edit');
    var editProp = element(by.repeater('p in properties.props'));
    editProp.element(by.id('editBtn')).click();
  });

  it('should be able to view property information', function() {
    element(by.model('search')).clear();
    element(by.model('search')).sendKeys('Some issues');
    element.all(by.css('.propGridItemPic')).last().click();
    expect(element(by.id('propName')).getText()).toEqual('Some issues');
    expect(element(by.id('propAddress')).getText()).toEqual('12 Prop Cr, PropTown');
  });

  it('should be able to to search for a property', function() {
    browser.get('/#/');
    element(by.model('search')).clear();
    element(by.model('search')).sendKeys('Some issues');
    
    var p = element.all(by.repeater('p in properties.props')).first();
    var pName = p.element(by.id('propName')).getText();
    expect(pName).toEqual('Some issues');
    logout();
  });
  
});

// financial system tests - NOT IMPLEMENTED
describe('Financial tests', function() {
  
});

// navigation
describe('Navigation tests', function() {
  it('should be able to navigate to the property page', function() {
    login('admin');
    element(by.css('.propGridItemPic')).click();
    logout();
  });
});
