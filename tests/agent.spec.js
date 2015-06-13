var login = function(user) {
  element(by.model('username')).clear();
  element(by.model('username')).sendKeys(user);
  element(by.model('password')).clear();
  element(by.model('password')).sendKeys(user);
  element(by.id('loginBtn')).click();
};

var model = function(m) {
  return element(by.model(m));
};

var logout = function() {
  element(by.id('logoutBtn')).click();
};

var tearDown = function() {
  element.all(by.id('resolvedRow')).each(function(i) {
    i.element(by.id('deleteBtn')).click();
  });

};

describe('Agent tests', function() {


  it('should login in an admin user', function() {
    login('admin'); 
    expect(browser.getCurrentUrl()).toEqual('http://localhost:8000/#/');
  });

  it('should allow an agent to go to a property page', function() {
    element(by.model('search')).sendKeys('All good');
    element(by.css('.propGridItemPic')).click();
    expect(element(by.id('propName')).getText()).toEqual('All Good');
  });

  it('should allow an agent to search for properties', function() {
    browser.get('/#/');
    element(by.model('search')).sendKeys('first');
    // should return 2 properties
    var props = element.all(by.repeater('p in properties.props'));

    props.count().then(function(data) {
      expect(data).toEqual(2);
    });
    
  });
  
  it('should allow an agent to search for properties and get no results', function() {
    browser.get('/#/');
    element(by.model('search')).sendKeys('fdsafdsafdsa');
    var props = element.all(by.repeater('p in properties.props'));

    props.count().then(function(data) {
      expect(data).toEqual(0);
    });
    
  });
  
  it('should be able to create a new property', function() {
    browser.get("/#/");

    element(by.id('createBtn')).click();
    // open modal
    var createModal = element(by.model('prop.address'));
    browser.wait(EC.visibilityOf(createModal), 5000);

    // create the test property
    element(by.model('prop.address')).sendKeys("12 AgentTest Ave, Propertyville");
    element(by.model('prop.name')).sendKeys("Agent Test Prop");
    element(by.id('submitBtn')).click();

    element(by.model('search')).sendKeys('Agent Test Prop');

    var p = element(by.repeater('p in properties.props'));
    var pName = p.element(by.id('propName')).getText();
    expect(pName).toEqual('Agent Test Prop');
  });
  
  it('should not be able to create a new property with invalid inputs', function() {
    browser.get("/#/");

    element(by.id('createBtn')).click();
    // open modal
    var createModal = element(by.model('prop.address'));
    browser.wait(EC.visibilityOf(createModal), 5000);

    // create the test property
    element(by.model('prop.address')).sendKeys("");
    element(by.model('prop.name')).sendKeys("Agent Test Prop");
    element(by.id('submitBtn')).click();

    browser.get('/#/');
    // THIS DOESNT WORK
  });
  
  // Schedule event for property.
  it('should allow an agent to schedule an event on a property', function() {
    expect(false).toEqual(true);
  });
  // Schedule event for property, invalid details
  it('should allow an agent to schedule an event on a property, invalid details given', function() {
    expect(false).toEqual(true);
  });
  // Edit property inputs
  it('should allow an agent to edit a property', function() {
    expect(false).toEqual(true);
  });
  // Edit property inputs invalid inputs.
  it('should not allow an agent to edit a property with invalid inputs', function() {
    expect(false).toEqual(true);
  });
  // Change rent status
  it('should allow an agent to change the rent status on a property', function() {
    expect(false).toEqual(true);
  });
  // Change rent status, invalid.
  it('should not allow an agent to change on a property to an invalid status', function() {
    expect(false).toEqual(true);
  });

  
  it('should create an issue with low severity', function() {
    
    element(by.model('search')).sendKeys('All good');
    element(by.css('.propGridItemPic')).click();

    element(by.id('createIssueBtn')).click();
    // wait for modal to open
    var modalEl = element(by.model('issue.severity'));
    browser.wait(EC.visibilityOf(modalEl), 5000);

    //crate low severity issue
    element(by.cssContainingText('option', 'Minor')).click();
    element(by.model('issue.severity')).click();
    model('issue.description').sendKeys("Minor");
    element(by.id('issueSubmit')).click();
    var issueDesc = element.all(by.css('.issueDescription'));
    // ensure the last element in the list is the new issue
    expect(issueDesc.last().getText()).toEqual('Minor');
  });

  it('should create an issue with moderate severity', function() {
    
    element(by.id('createIssueBtn')).click();
    // wait for modal to open
    var modalEl = element(by.model('issue.severity'));
    browser.wait(EC.visibilityOf(modalEl), 5000);

    //crate low severity issue
    element(by.cssContainingText('option', 'Moderate')).click();
    element(by.model('issue.severity')).click();
    model('issue.description').sendKeys("Moderate");
    element(by.id('issueSubmit')).click();
    var issueDesc = element.all(by.css('.issueDescription'));
    // ensure the last element in the list is the new issue
    expect(issueDesc.last().getText()).toEqual('Moderate');
  });
  
  it('should create an issue with high severity', function() {
    
    element(by.id('createIssueBtn')).click();
    // wait for modal to open
    var modalEl = element(by.model('issue.severity'));
    browser.wait(EC.visibilityOf(modalEl), 5000);

    //crate low severity issue
    element(by.cssContainingText('option', 'Severe')).click();
    element(by.model('issue.severity')).click();
    model('issue.description').sendKeys("Severe");
    element(by.id('issueSubmit')).click();
    var issueDesc = element.all(by.css('.issueDescription'));
    // ensure the last element in the list is the new issue
    expect(issueDesc.last().getText()).toEqual('Severe');
  });
  
  it('should not let an issue with invalid details be created', function() {
    
    // FIX TBD
    element(by.id('createIssueBtn')).click();
    // wait for modal to open
    var modalEl = element(by.model('issue.severity'));
    browser.wait(EC.visibilityOf(modalEl), 5000);

    //crate low severity issue
    element(by.cssContainingText('option', 'Severe')).click();
    element(by.model('issue.severity')).click();
    // model('issue.description').sendKeys("Severe");
    element(by.id('issueSubmit')).click();
    var issueDesc = element.all(by.css('.issueDescription'));
    
    // ensure the last element in the list is the new issue
    // expect(issueDesc.last().getText()).toEqual('Severe');

    // clear the modal
    element(by.id('cancelBtn')).click();
    
  });
  
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

  it('should enable a agent to search for an issue', function() {
    // Search for the "Minor" issue created earlier
    element(by.id('issueSearch')).clear();
    element(by.id('issueSearch')).sendKeys('Minor');
    var issueDesc = element.all(by.css('.issueDescription'));
    expect(issueDesc.last().getText()).toEqual('Minor');
  });
  
  it('should enable a agent to search for an issue, with no results', function() {
    // Search for the "Minor" issue created earlier
    element(by.id('issueSearch')).clear();
    element(by.id('issueSearch')).sendKeys('fdsafdsa');
    var issueDesc = element.all(by.css('.issueDescription'));

    issueDesc.count().then(function(data) {
      expect(data).toEqual(0);
    });
    
  });
  
  it('should allow a agent to resolve an issue', function() {
    element(by.id('issueSearch')).clear();
    element(by.id('issueSearch')).sendKeys('Minor');
    var issue = element(by.css('.issueRow'));
    issue.element(by.id('resolveBtn')).click();
    tearDown();
    logout();
  });
  
  // Search for issue, no results.
});
