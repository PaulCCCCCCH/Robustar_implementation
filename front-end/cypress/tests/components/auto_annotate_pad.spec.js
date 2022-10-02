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
    cy.clickBySel('auto-annotate-pad-start-auto-annotation');
    cy.wait(20000);
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
    cy.get('p').should('have.text', 'No task is running now.');
  });

  it('Test Input Zero', () => {
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('auto-annotate-end-index').clear().type('0');
    cy.clickBySel('auto-annotate-pad-start-auto-annotation');
    cy.get('p').should('have.text', 'No task is running now.');
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
    cy.get('p').should('have.text', 'No task is running now.');
  });

  it('Test Start index be negative number', () => {
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('auto-annotate-start-index').clear().type('-1');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.get('p').should('have.text', 'No task is running now.');
  });

  it('Test End index be less than -1', () => {
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('auto-annotate-end-index').clear().type('-2');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.get('p').should('have.text', 'No task is running now.');
  });

  it('Test End index be less than Start index', () => {
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('auto-annotate-start-index').clear().type('99999');
    cy.getBySel('auto-annotate-end-index').clear().type('99998');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.get('p').should('have.text', 'No task is running now.');
  });
});
