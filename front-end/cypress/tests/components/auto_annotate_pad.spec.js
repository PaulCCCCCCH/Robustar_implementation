describe('Auto Annotate Pad', () => {
  after(() => {
    cy.visit('http://localhost:8080/#/image-list/annotated');
    cy.getBySel('image-list-btn-clear-annotated-imgs').click();
    cy.wait(500);
  });

  beforeEach(() => {
    cy.visit('http://localhost:8080/#/image-list/annotated');
    cy.getBySel('image-list-btn-clear-annotated-imgs').click();
    cy.wait(500);
    cy.visit('http://localhost:8080/#/auto-annotate');
    cy.wait(500);
  });

  it('Test Annotated Images url', () => {
    cy.getBySel('auto-annotate-start-index').clear().type('1');
    cy.getBySel('auto-annotate-end-index').clear().type('3');
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();

    // This will wait for max 120 seconds until the task is finished
    cy.get('task-panel-stop-task'); // Wait until task pops up
    cy.get('[data-test=task-center-p-no-task]', { timeout: 120 * 1000 });

    cy.contains('Inspect Data').click();
    cy.contains('Annotated Data').click();
    cy.url().should('include', '/image-list/annotated');
    cy.getBySel('image-list-div-img').should('have.length', 2);
    cy.getBySel('image-list-img-1').trigger('mouseenter');
    cy.clickBySel('image-list-btn-edit-image-1');
    cy.checkSessionStorage('split', 'annotated');
  });

  it('Delete the Only One Task', () => {
    cy.clickBySel('header-toggle-tasks-panel');
    cy.getBySel('auto-annotate-end-index').clear().type('500');
    cy.clickBySel('auto-annotate-pad-start-auto-annotation');
    cy.getBySel('task-panel-item-name').children().should('have.length', 1);
    cy.clickBySel('task-panel-stop-task');
    cy.getBySel('task-center-p-no-task').should('be.visible');
  });

  it('Test Input Zero', () => {
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('auto-annotate-end-index').clear().type('0');
    cy.clickBySel('auto-annotate-pad-start-auto-annotation');
    cy.getBySel('task-center-p-no-task').should('be.visible');
  });

  it('Test Input Zero Before Integer', () => {
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('auto-annotate-end-index').clear().type('0999').click();
    cy.clickBySel('auto-annotate-pad-start-auto-annotation');
    cy.getBySel('task-panel-progress-linear').should('contain', '999');
    cy.clickBySel('task-panel-stop-task');
  });

  it('Test Input Big Integer', () => {
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('auto-annotate-end-index').clear().type('9999');
    cy.clickBySel('auto-annotate-pad-start-auto-annotation');
    cy.getBySel('task-panel-item-name').children().should('have.length', 1);
    cy.getBySel('task-panel-progress-linear').should('contain', '9000');
    cy.clickBySel('task-panel-stop-task');
  });

  it('Test Input Floating Point Number', () => {
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('auto-annotate-end-index').clear().type('9.9');
    cy.clickBySel('auto-annotate-pad-start-auto-annotation');
    cy.getBySel('task-center-p-no-task').should('be.visible');
  });

  it('Test Start index be negative number', () => {
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('auto-annotate-start-index').clear().type('-1');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.getBySel('task-center-p-no-task').should('be.visible');
  });

  it('Test End index be less than -1', () => {
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('auto-annotate-end-index').clear().type('-2');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.getBySel('task-center-p-no-task').should('be.visible');
  });

  it('Test End index be less than Start index', () => {
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('auto-annotate-start-index').clear().type('99999');
    cy.getBySel('auto-annotate-end-index').clear().type('99998');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.getBySel('task-center-p-no-task').should('be.visible');
  });
});
