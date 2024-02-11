describe('The Model Training Page', () => {
  beforeEach(() => {
    cy.visit('model');
  });

  it('can have current model after selecting', () => {
    cy.get('tr:nth-child(1)').find('td').eq(10).within(() => {
      cy.get('[data-test=train-model-edit-model]').click({ force: true });
    })
      cy.getBySel('train-model-set-current-model').click();
      cy.wait(1000);
      cy.getBySel('train-model-current-model-create-time').should('not.be.empty');
      cy.getBySel('train-model-current-model-achitecture').should('not.be.empty');

  });

  it('can go to the train page after having current model', () => {
    cy.get('tr:nth-child(1)').find('td').eq(10).within(() => {
      cy.get('[data-test=train-model-edit-model]').click({ force: true });
    });
    cy.get('[data-test=train-model-set-current-model]').click();
    cy.wait(1000);
    cy.get('[data-test=train-model-edit-model-cancel]').click();
    cy.get('[data-test=train-model-train-model-button]').click();
    cy.url().should('contains', 'train');
  });

  it('can edit model', () => {
    cy.get('tr:nth-child(1)').find('td').eq(10).within(() => {
      cy.get('[data-test=train-model-edit-model]').click({ force: true });
    });

    cy.get('[data-test=train-model-edit-model-description]').clear().type("test123");
    cy.get('[data-test=train-model-edit-model-cancel]').click();

    cy.get('tr:nth-child(1)').find('td').eq(10).within(() => {
      cy.get('[data-test=train-model-edit-model]').click({ force: true });
    });
    cy.get('[data-test=train-model-edit-model-description]').invoke('val').should('not.contain', 'test123');
    cy.get('tr:nth-child(1)').find('td').eq(10).within(() => {
      cy.get('[data-test=train-model-edit-model]').click({ force: true });
    });

    cy.get('[data-test=train-model-edit-model-description]').clear().type("test");
    cy.get('[data-test=train-model-edit-model-confirm]').click();
    cy.get('tr:nth-child(1)').find('td').eq(10).within(() => {
      cy.get('[data-test=train-model-edit-model]').click({ force: true });
    });
    cy.get('[data-test=train-model-edit-model-description]').invoke('val').should('contain', 'test');
  });

  it('can duplicate model', () => {
    cy.get('tr:nth-child(1)').find('td').eq(10).within(() => {
      cy.get('[data-test=train-model-duplicate-model]').click();
      cy.wait(1000);
    });
    cy.get('tr').should('have.length', 3);
  });


  it('can delete model', () => {
    cy.get('tr:nth-child(1)').find('td').eq(10).within(() => {
      cy.get('[data-test=train-model-delete-model]').click();
    });

    cy.get('[data-test=train-model-delete-model-confirm]').click();
    cy.wait(1000);
    cy.get('tr').should('have.length', 2);

  });



  it('can upload model', () => {
    cy.contains('.v-btn', 'Upload New Model').click();
    cy.get('[data-test=model-upload-nickname]').type("SimpleCNN");
    cy.get('[data-test=model-upload-classname]').type("SimpleCNN");
    cy.get('[data-test=model-upload-codefile]').selectFile('cypress/downloads/SimpleCNN.py', { force: true });
    cy.get('[data-test=model-upload-submit-button]').click();
    cy.get('tr').should('have.length', 3);


  });


  it('can edit model name', () => {
    cy.get('tr:nth-child(1)').find('td').eq(10).within(() => {
      cy.get('[data-test=train-model-edit-model]').click({ force: true });
    });

    cy.get('[data-test=train-model-edit-model-name]').clear().type("test");
    cy.get('[data-test=train-model-edit-model-confirm]').click();

    cy.get('[data-test=train-model-edit-model-name]').invoke('val').should('contain', 'test');
  });
});