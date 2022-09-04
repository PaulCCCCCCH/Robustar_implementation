describe('Annotation Pad (Image Editor)', () => {
  before(() => {
    cy.visit('/');
    cy.contains('Inspect Data').click();
    cy.contains('Annotated Data').click();
    cy.getBySel('image-list-btn-clear-annotated-imgs').click();
    cy.wait(500);
  });

  beforeEach(() => {
    cy.visit('image-list/train');
  });

  after(() => {
    cy.visit('/');
    cy.contains('Inspect Data').click();
    cy.contains('Annotated Data').click();
    cy.getBySel('image-list-btn-clear-annotated-imgs').click();
    cy.wait(500);
  });

  it('Enables editing images in training set', () => {
    cy.getBySel('image-list-img-0').trigger('mouseenter');
    cy.getBySel('image-list-btn-edit-image-0').click();
    cy.checkSessionStorage('split', 'train');

    cy.wait(1000);
    const strs = ['1.JPEG', '10.JPEG', '100.JPEG'];
    Cypress._.times(3, (index) => {
      cy.get('.tui-image-editor-send-edit-btn').click();
      cy.wait(1000);
      cy.get('.tui-image-editor').should('exist');
      cy.checkSessionStorageSubString('image_url', strs[index]);
    });
  });

  it('Enables editing images in annotated set', () => {
    const strs = ['1.JPEG', '10.JPEG', '0.JPEG'];
    cy.visit('image-list/annotated');

    cy.getBySel('image-list-div-img').should('have.length', 3);

    cy.getBySel('image-list-img-0').trigger('mouseenter');
    cy.getBySel('image-list-btn-edit-image-0').click();
    cy.checkSessionStorage('split', 'annotated');

    cy.wait(1000);
    Cypress._.times(3, (index) => {
      cy.get('.tui-image-editor-send-edit-btn').click();
      cy.wait(1000);
      cy.checkSessionStorageSubString('image_url', strs[index]);
    });
  });
});
