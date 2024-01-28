describe('The Model Training Page', () => {
  beforeEach(() => {
    cy.visit('model');
  });

  it('can have current model after selecting', () => {
    cy.get('tr:first-child').first().within(() => {
      cy.get('[data-test=trian-model-set-current-model]').click();
    });
    cy.wait(1000);
    cy.getBySel('train-model-current-model-create-time').should('not.be.empty');
    cy.getBySel('train-model-current-model-achitecture').should('not.be.empty');
  });

  it('can go to the train page after having current model', () => {
    cy.get('tr:first-child').first().within(() => {
      cy.get('[data-test=trian-model-set-current-model]').click();
    });
    cy.wait(1000);
    cy.get('[data-test=train-model-current-model]')
      .should('exist')
      .invoke('text')
      .should('not.be.empty');
    cy.get('[data-test=train-model-train-currentq-model]').click();
    cy.url().should('inlcude', 'train');
  });

  it('Triggers model training', () => {
    cy.intercept('POST', '/api/train-model/**').as('trainModel');
    cy.getBySel('[data-test=train-model-train-model-button]').click();
    cy.wait('@trainModel').its('response.statusCode').should('eq', 200);
  });

  it('can edit model', () => {
    cy.get('tr:first-child').first().within(() => {
      cy.get('[data-test=trian-model-edit-model]').click();
      cy.wait(1000);
      cy.getBySel('[data-test=train-model-train-model-edit-model-description]').empty();
      cy.getBySel('[data-test=rain-model-train-model-edit-model-description]').type("test123");
      cy.get('[data-test=train-model-edit-model-cancel]').click();
      cy.getBySel('[data-test=train-model-current-model-description]').should('not.contain', 'test123');


      cy.get('[data-test=trian-model-edit-model]').click();
      cy.wait(1000);
      cy.getBySel('[data-test=train-model-train-model-edit-model-description]').empty();
      cy.getBySel('[data-test=rain-model-train-model-edit-model-description]').type("test");
      cy.get('[data-test=train-model-edit-model-confirm]').click();
      cy.getBySel('[data-test=train-model-current-model-description]').should('inlcude', 'test123');
    });

  });

  it('can duplicate model', () => {
    cy.get('tr:first-child').first().within(() => {
      cy.get('[data-test=trian-model-duplicate-model]').click();
      cy.wait(1000);
    });
    cy.get('tr:nth-child(2)').should('inlcude', 'copy');
  });

  it('can delete model', () => {
    cy.get('tr:first-child').first().within(() => {
      cy.get('[data-test=trian-model-delete-model]').click();  
    });
    cy.wait(1000);
    cy.get('tr:first-child').first().within(() => {
      cy.get('[data-test=trian-model-delete-model]').click();
      cy.wait(1000);
    });
  });


});
