describe('Train Pad', () => {
  beforeEach(() => {
    cy.visit('train-pad');
  });

  it('Test training with default settings', () => {
    cy.getBySel('train-pad-start-btn').click();
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('task-panel-stop-task').click();
    cy.getBySel('task-center-p-no-task');
  });

  it('Test stopping on-going training', () => {
    cy.getBySel('train-pad-start-btn').click();
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('task-panel-stop-task');
    cy.getBySel('train-pad-stop-btn').click();
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('task-center-p-no-task');
  });

  // it('Delete the Only One Task', () => {
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('auto-annotate-end-index').clear().type('500');
  //   cy.clickBySel('auto-annotate-pad-start-auto-annotation');
  //   cy.clickBySel('header-toggle-tasks-panel');
  //   cy.getBySel('task-panel-item-name').children().should('have.length', 1);
  //   cy.getBySel('task-panel-stop-task').click();
  //   cy.getBySel('task-center-p-no-task').should('be.visible');
  // });

  // it('Test Input Zero', () => {
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('auto-annotate-end-index').clear().type('0');
  //   cy.clickBySel('auto-annotate-pad-start-auto-annotation');
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('task-center-p-no-task').should('be.visible');
  // });

  // it('Test Input Zero Before Integer', () => {
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('auto-annotate-end-index').clear().type('0999').click();
  //   cy.clickBySel('auto-annotate-pad-start-auto-annotation');
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('task-panel-progress-linear').should('contain', '999');
  //   cy.getBySel('task-panel-stop-task').click();
  //   cy.getBySel('task-center-p-no-task').should('be.visible');
  // });

  // it('Test Input Big Integer', () => {
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('auto-annotate-end-index').clear().type('9999');
  //   cy.clickBySel('auto-annotate-pad-start-auto-annotation');
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('task-panel-item-name').children().should('have.length', 1);
  //   cy.getBySel('task-panel-progress-linear').should('contain', '9000');
  //   cy.getBySel('task-panel-stop-task').click();
  //   cy.getBySel('task-center-p-no-task').should('be.visible');
  // });

  // it('Test Input Floating Point Number', () => {
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('auto-annotate-end-index').clear().type('9.9');
  //   cy.clickBySel('auto-annotate-pad-start-auto-annotation');
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('task-center-p-no-task').should('be.visible');
  // });

  // it('Test Start index be negative number', () => {
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('auto-annotate-start-index').clear().type('-1');
  //   cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('task-center-p-no-task').should('be.visible');
  // });

  // it('Test End index be less than -1', () => {
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('auto-annotate-end-index').clear().type('-2');
  //   cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('task-center-p-no-task').should('be.visible');
  // });

  // it('Test End index be less than Start index', () => {
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('auto-annotate-start-index').clear().type('99999');
  //   cy.getBySel('auto-annotate-end-index').clear().type('99998');
  //   cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
  //   cy.getBySel('header-toggle-tasks-panel').click();
  //   cy.getBySel('task-center-p-no-task').should('be.visible');
  // });
});
