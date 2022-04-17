describe('Auto Annotate Pad', () => {
  before(() => {
    cy.visit('http://localhost:8080/#/auto-annotate');
  });
  it('Test Auto Annotation Button', () => {
    cy.get('[data-test = auto-annotate-input-sample-per-class]').clear();
    cy.get('[data-test = auto-annotate-input-sample-per-class]').type('50');
    cy.get('[data-test = auto-annotate-pad-start-auto-annotation]').click();
  });

  it('Test Task Panel', () => {
    cy.get('[data-test = header-toggle-tasks-panel]').click();
    cy.wait(10000);
    cy.get('[data-test = task-panel-stop-task]').click();
    cy.get('p').should('have.text', 'No task is running now.');
    cy.get('[data-test = header-toggle-tasks-panel]').click();
  });

  it('Test Auto Annotation Button2', () => {
    cy.get('[data-test = auto-annotate-input-sample-per-class]').clear();
    cy.get('[data-test = auto-annotate-input-sample-per-class]').type('5');
    cy.get('[data-test = auto-annotate-pad-start-auto-annotation]').click();
  });
  it('Test Task Panel2', () => {
    cy.wait(4000);
    cy.get('[data-test = header-toggle-tasks-panel]').click();
    cy.getBySel('task-panel-item-name').children().should('have.length', 1);

    // reopen the task panel
    cy.get('[data-test = header-toggle-tasks-panel]').click();
    cy.get('[data-test = header-toggle-tasks-panel]').click();
    cy.get('p').should('have.text', 'No task is running now.');
  });
  it('Test Annotated Images url', () => {
    cy.contains('Inspect Data').click();
    cy.contains('Annotated Data').click();
    cy.url().should('include', '/image-list/annotated');
    cy.getBySel('image-list-div-all-imgs').children().should('have.length', 5);
    cy.getBySel('image-list-img-1').trigger('mouseenter');
  });
});
