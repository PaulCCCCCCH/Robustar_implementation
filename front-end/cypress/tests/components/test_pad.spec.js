describe('The Test Page', () => {
  beforeEach(() => {
    cy.visit('test');
  });

  it('can test on validation set one task at a time', () => {
    // Clicking on test multiple times should only spawn one test task because the model is locked
    cy.getBySel('test-pad-btn-test-on-validation-set').click();
    cy.getBySel('test-pad-btn-test-on-validation-set').click();
    cy.getBySel('test-pad-btn-test-on-validation-set').click();
    cy.getBySel('test-pad-btn-test-on-test-set').click();
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('task-panel-item-name').children().should('have.length', 1);

    // wait for maximum 120 seconds for the test to finish
    cy.get('[data-test=task-panel-task-done]', { timeout: 120 * 1000 }).click();
  });

  it('can set correctly and incorrectly classified samples in image list', () => {
    // Go to image list page
    cy.visit('http://localhost:8080/#/image-list/validation');

    // Locate classification filter dropdown
    cy.getBySel('image-list-select-classification').as('classification');

    // Expect some correctly classified images
    cy.get('@classification').click({ force: true });
    cy.contains('Correctly Classified').click();
    cy.getBySel('image-list-div-all-imgs').children().should('have.length.least', 1);

    // Expect some incorrectly classified images
    cy.get('@classification').click({ force: true });
    cy.contains('Incorrectly Classified').click();
    cy.getBySel('image-list-div-all-imgs').children().should('have.length.least', 1);
  });
});
