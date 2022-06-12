describe('Auto Annotate Pad', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8080/#/auto-annotate');
  });

  it('Test Annotated Images url', () => {
    cy.getBySel('auto-annotate-start-index').clear().type('1');
    cy.getBySel('auto-annotate-end-index').clear().type('5');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.wait(3000);
    cy.contains('Inspect Data').click();
    cy.contains('Annotated Data').click();
    cy.url().should('include', '/image-list/annotated');
    cy.getBySel('image-list-div-all-imgs').children().should('have.length', 8);
    cy.getBySel('image-list-img-2').trigger('mouseenter');
    cy.getBySel('image-list-btn-edit-image-2').click();
    cy.checkSessionStorage('split', 'annotated');

  });

  it('Delete the Only One Task', () => {
    cy.getBySel('auto-annotate-end-index').clear().type('500');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('task-panel-item-name').children().should('have.length', 1);
    cy.getBySel('task-panel-stop-task').click();
    cy.get('p').should('have.text', 'No task is running now.');
  });

  it('Test Input Zero', () => {
    cy.getBySel('auto-annotate-end-index').clear().type('0');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.getBySel('header-toggle-tasks-panel').click()
    cy.get('p').should('have.text', 'No task is running now.');
  });

  it('Test Input Zero Before Integer', () => {
    cy.getBySel('auto-annotate-end-index').clear().type('010').click();
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();

    cy.getBySel('header-toggle-tasks-panel').click()
    cy.getBySel('task-panel-progress-linear').should('contain', "10")
    cy.getBySel('task-panel-stop-task').click();
  });


  it('Test Input Big Integer', () => {
    cy.getBySel('auto-annotate-end-index').clear().type('9999');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.getBySel('header-toggle-tasks-panel').click()
    cy.getBySel('task-panel-item-name').children().should('have.length', 1);
    cy.getBySel('task-panel-progress-linear').should('contain', "9000")
    cy.getBySel('task-panel-stop-task').click();
  });

  it('Test Input Floating Point Number', () => {
    cy.getBySel('auto-annotate-end-index').clear().type('9.9');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.getBySel('header-toggle-tasks-panel').click()
    cy.get('p').should('have.text', 'No task is running now.');
  });

  it('Test Start index be negative number', () => {
    cy.getBySel('auto-annotate-start-index').clear().type('-1');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.getBySel('header-toggle-tasks-panel').click()
    cy.get('p').should('have.text', 'No task is running now.');
  });

  it('Test End index be less than -1', () => {
    cy.getBySel('auto-annotate-end-index').clear().type('-2');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.getBySel('header-toggle-tasks-panel').click()
    cy.get('p').should('have.text', 'No task is running now.');
  });


  it('Test End index be less than Start index', () => {
    cy.getBySel('auto-annotate-start-index').clear().type('99999');
    cy.getBySel('auto-annotate-end-index').clear().type('99998');
    cy.getBySel('auto-annotate-pad-start-auto-annotation').click();
    cy.getBySel('header-toggle-tasks-panel').click()
    cy.get('p').should('have.text', 'No task is running now.');
  })
});