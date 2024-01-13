describe('The Model Training Page', () => {
  beforeEach(() => {
    cy.visit('model');
  });

  it('can have current model after selecting', () => {
    cy.get('tr:first-child').within(() => {
      cy.get('[data-test=trian-model-set-current-model]').click();
    });
    cy.wait(1000);
    cy.get('[data-test=train-model-current-model]')
      .should('exist')
      .invoke('text')
      .should('not.be.empty');
  });

  it('can go to the train page after having current model', () => {
    cy.get('tr:first-child').within(() => {
      cy.get('[data-test=trian-model-set-current-model]').click();
    });
    cy.wait(1000);
    cy.get('[data-test=train-model-current-model]')
      .should('exist')
      .invoke('text')
      .should('not.be.empty');
    cy.get('[data-test=train-model-train-current-model]').click();
    cy.url().should('inlcude', 'train');
  });
});
