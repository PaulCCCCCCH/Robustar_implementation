describe('Annotation Pad (Image Editor)', () => {
  beforeEach(() => {});

  it('Goes to the page for the target', () => {
    cy.contains('Class Name').click({ force: true });
    cy.contains('cat').click();
    cy.contains('GOTO CLASS').click();

    cy.getBySel('image-list-input-page-number').as('page-num').should('have.value', 125);
    cy.getBySel('image-list-btn-next-page').as('next-page').click();
    cy.get('@next-page').click();
    cy.get('@page-num').should('have.value', 127);

    cy.get('@page-num').type('9999');
    cy.contains('GOTO PAGE').click();

    cy.get('@page-num').should('have.value', 1124);

    cy.getBySel('image-list-img-1').trigger('mouseenter');
    cy.getBySel('image-list-btn-edit-image-1').click();
    cy.checkSessionStorage('split', 'train');
    // cy.checkSessionStorage('annotated', '0')

    cy.wait(1000);
    cy.get('.tui-image-editor-send-edit-btn').click();
    cy.wait(1000);
    cy.get('.tui-image-editor-send-edit-btn').click();
    cy.wait(1000);
    cy.get('.tui-image-editor-send-edit-btn').click();
    cy.wait(1000);

    cy.visit('http://localhost:8080/#/image-list/annotated');
    // cy.getBySel("image-list-div-all-imgs").children().should('have.length', 3)

    cy.visit('http://localhost:8080/#/auto-annotate');
    cy.getBySel('auto-annotate-input-sample-per-class').type('5');

    cy.contains('START AUTO ANNOTATION').click();
    cy.wait(10000);

    cy.visit('http://localhost:8080/#/image-list/annotated');
    cy.getBySel('image-list-div-all-imgs').children().should('have.length', 8);

    cy.visit('http://localhost:8080/#/image-list/train');
    cy.getBySel('image-list-img-1').trigger('mouseenter');
    cy.wait(1000);
    cy.getBySel('image-list-btn-edit-image-1').click();
    cy.wait(1000);

    cy.visit('http://localhost:8080/#/image-list/annotated');
    cy.getBySel('image-list-div-all-imgs').children().should('have.length', 8);
  });
});
