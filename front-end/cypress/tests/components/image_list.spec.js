describe('Image List (Image Editor)', () => {
  beforeEach(() => {});

  it('Navigates through training data', () => {
    cy.visit('http://localhost:8080/#/image-list/train');

    // define elements
    cy.getBySel('image-list-select-class-name').as('class-name-dropdown');
    cy.getBySel('image-list-input-page-number').as('page-num');
    cy.getBySel('image-list-btn-next-page').as('next-page');
    cy.getBySel('image-list-btn-prev-page').as('prev-page');

    cy.get('@page-num').should('have.value', 0);
    cy.checkSessionStorage('train', '0');

    cy.get('@next-page').click();
    cy.get('@next-page').click();

    cy.get('@page-num').should('have.value', 2);
    cy.checkSessionStorage('train', '2');

    cy.get('@class-name-dropdown').click({ force: true });
    cy.contains('cat').click();
    cy.contains('GOTO CLASS').click();

    cy.get('@page-num').should('have.value', 125);
    cy.get('@next-page').click();
    cy.get('@next-page').click();
    cy.get('@page-num').should('have.value', 127);

    cy.get('@page-num').type('9999');
    cy.contains('GOTO PAGE').click();

    cy.get('@page-num').should('have.value', 1124);

    cy.get('@prev-page').click();
    cy.get('@prev-page').click();

    cy.get('@page-num').should('have.value', 1122);
    cy.checkSessionStorage('train', '1122');

    cy.getBySel('image-list-img-1').trigger('mouseenter');
    cy.getBySel('image-list-btn-edit-image-1').click();
    cy.checkSessionStorage('split', 'train');
    cy.wait(300);
    cy.go('back');
    cy.wait(300);
  });

  it('Navigates through validation data', () => {
    cy.visit('http://localhost:8080/#/image-list/validation');

    cy.wait(300);
    // define elements
    cy.getBySel('image-list-select-class-name').as('class-name-dropdown');
    cy.getBySel('image-list-input-page-number').as('page-num');
    cy.getBySel('image-list-btn-next-page').as('next-page');
    cy.getBySel('image-list-btn-prev-page').as('prev-page');
    cy.getBySel('image-list-select-classification').as('classification');

    cy.get('@page-num').should('have.value', 0);
    cy.checkSessionStorage('train', '1122');
    cy.checkSessionStorage('validation_correct', '0');

    cy.get('@classification').click({ force: true });
    cy.contains('Incorrectly Classified').click();

    cy.getBySel('image-list-div-all-imgs').children().should('have.length', 8);

    cy.get('@page-num').type('9999');
    cy.contains('GOTO PAGE').click();

    cy.get('@next-page').should('be.disabled');

    cy.get('@classification').click({ force: true });
    cy.contains('Correctly Classified').click();

    cy.getBySel('image-list-div-all-imgs').children().should('have.length', 8);
    cy.get('@page-num').should('have.value', 0);
  });
});
