describe('Train Pad', () => {
  it('Test training with default settings and stop training', () => {
    cy.visit('train-pad');

    // Clicking on train multiple times should only spawn one test task because the model is locked
    cy.getBySel('train-pad-start-btn').click();
    cy.getBySel('train-pad-start-btn').click();
    cy.getBySel('train-pad-start-btn').click();
    cy.getBySel('header-toggle-tasks-panel').click();

    // Wait for maximum 120 seconds for the training to start and the progress to pop up
    cy.getBySel('task-panel-item-name', { timeout: 60 * 1000 })
      .children()
      .should('have.length', 1);
    cy.get('[data-test=task-panel-progress-linear]', { timeout: 60 * 1000 }).should(
      'not.contain',
      'UNKNOWN'
    );

    // Stop training and wait for 20 seconds for the task center to clean up
    cy.getBySel('train-pad-stop-btn').click();
    cy.getBySel('header-toggle-tasks-panel').click();
    cy.getBySel('task-center-p-no-task', { timeout: 20 * 1000 }).should('be.visible');
  });
});
