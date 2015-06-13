var model = function(m) {
  return element(by.model(m));
};

var logout = function() {
  element(by.id('logoutBtn')).click();
};

describe('Tenant tests', function() {
  var loginTenant = function() {
    element(by.model('username')).clear();
    element(by.model('username')).sendKeys("tenant");
    element(by.model('password')).clear();
    element(by.model('password')).sendKeys("tenant");
    element(by.id('loginBtn')).click();
  };

  it('should redirect to the tenant property on login', function() {
    browser.get('/#/login');
    loginTenant();
    // this is the default tenant who rents thed "Some Issues" property
    expect(element(by.id('propName')).getText()).toEqual('Some issues');
  });

  it('should create an issue with low severity', function() {
    
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
  });
  
  it('should be able to remove an issue', function() {
    browser.get('/#/');
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

  it('should enable a tenant to search for an issue', function() {
    // Search for the "Minor" issue created earlier
    element(by.id('issueSearch')).sendKeys('Minor');
    var issueDesc = element.all(by.css('.issueDescription'));
    expect(issueDesc.last().getText()).toEqual('Minor');
  });

  it('should allow a tenant to resolve an issue', function() {
    element(by.id('issueSearch')).clear();
    element(by.id('issueSearch')).sendKeys('Severe');
    var issue = element(by.css('.issueRow'));
    issue.element(by.id('resolveBtn')).click();
    logout();
  });
  
});
