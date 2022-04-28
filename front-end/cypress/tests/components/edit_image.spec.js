describe('Annotation Pad (Image Editor)', () => {
  beforeEach(() => {});

  it('Enables editing images in training set', () => {
    cy.visit(Cypress.env('base_url') + 'image-list/train');

    cy.getBySel('image-list-img-0').trigger('mouseenter');
    cy.getBySel('image-list-btn-edit-image-0').click();
    cy.checkSessionStorage('split', 'train');

    Cypress._.times(3, (index) => {
      cy.get('.tui-image-editor-send-edit-btn').click();
      cy.wait(1000);
      cy.checkSessionStorage('image_id', index + 1);
    });
  });

  it('Enables editing images in annotated set', () => {
    cy.visit(Cypress.env('base_url') + 'image-list/annotated');

    cy.getBySel('image-list-div-all-imgs').children().should('have.length', 3);

    cy.getBySel('image-list-img-0').trigger('mouseenter');
    cy.getBySel('image-list-btn-edit-image-0').click();
    cy.checkSessionStorage('split', 'annotated');

    cy.wait(1000);
    Cypress._.times(3, (index) => {
      cy.get('.tui-image-editor-send-edit-btn').click();
      cy.wait(1000);
      cy.checkSessionStorage('image_id', index + 1);
    });

    cy.visit(Cypress.env('base_url') + 'image-list/annotated');
  });
});
