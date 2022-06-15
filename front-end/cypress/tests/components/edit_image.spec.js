describe('Annotation Pad (Image Editor)', () => {
  beforeEach(() => {});

  it('Enables editing images in training set', () => {
    cy.visit('image-list/train');
    cy.wait(3000);
    cy.getBySel('image-list-img-0').trigger('mouseenter');
    cy.getBySel('image-list-btn-edit-image-0').click();
    cy.checkSessionStorage('split', 'train');
    cy.get('.tui-image-editor').should('exist');

    Cypress._.times(3, (index) => {
      cy.get('.tui-image-editor-send-edit-btn').click();
      cy.get('.tui-image-editor').should('exist');
      cy.checkSessionStorage('image_id', index + 1);
    });
  });

  it('Enables editing images in annotated set', () => {
    cy.visit('image-list/annotated');

    cy.getBySel('image-list-div-all-imgs').children().should('have.length', 3);

    cy.getBySel('image-list-img-0').trigger('mouseenter');
    cy.getBySel('image-list-btn-edit-image-0').click();
    cy.checkSessionStorage('split', 'annotated');

    Cypress._.times(3, (index) => {
      cy.wait(1000);
      cy.get('.tui-image-editor-send-edit-btn').click();
      cy.checkSessionStorage('image_id', index + 1);
    });

    cy.visit('image-list/annotated');
  });
});
