describe('Image List', () => {
  beforeEach(() => {});

  it('Navigates through training data', () => {
    cy.visit('http://localhost:8080/#/image-list/train');
    // TODO: What to invoke to get page number? Hard coding 12 for now.
    cy.getBySel('image-list-input-num-per-page')
      .invoke('val')
      .then((text) => {
        // define elements
        cy.getBySel('image-list-select-class-name').as('class-name-dropdown');
        cy.getBySel('image-list-input-page-number').as('page-num');
        cy.getBySel('image-list-btn-next-page').as('next-page');
        cy.getBySel('image-list-btn-prev-page').as('prev-page');

        cy.get('@page-num').clear().type('0');
        cy.contains('GOTO PAGE').click();

        // cy.get('@page-num').should('have.value', 0);
        // cy.reload()
        // cy.checkSessionStorageObj('image_page_history', 'train', 0);

        cy.get('@next-page').click();
        cy.get('@next-page').click();
        cy.get('@page-num').should('have.value', 2);
        cy.reload();
        cy.checkSessionStorageObj('image_page_history', 'train', 2);

        cy.get('@class-name-dropdown').click({ force: true });
        cy.contains('cat').click();
        cy.contains('GOTO CLASS').click();

        // TODO: hardcoded for now
        const num_per_page = 12;
        const currPage = Math.ceil(1000 / num_per_page) - 1;
        cy.get('@page-num').should('have.value', currPage);
        cy.get('@next-page').click();
        cy.get('@next-page').click();
        cy.get('@page-num').should('have.value', currPage + 2);

        cy.get('@page-num').clear().type('9999');
        cy.contains('GOTO PAGE').click();

        const maxPage = Math.ceil(9000 / num_per_page) - 1;
        cy.get('@page-num').should('have.value', maxPage);

        cy.get('@prev-page').click();
        cy.get('@prev-page').click();

        cy.get('@page-num').should('have.value', maxPage - 2);
        cy.reload();
        cy.checkSessionStorageObj('image_page_history', 'train', maxPage - 2);

        cy.getBySel('image-list-img-1').trigger('mouseenter');
        cy.getBySel('image-list-btn-edit-image-1').click();
        cy.reload();
        cy.checkSessionStorage('image_split', 'train');
      });
  });

  it('Navigates through validation data', () => {
    cy.visit('http://localhost:8080/#/image-list/validation');

    // define elements
    cy.getBySel('image-list-select-class-name').as('class-name-dropdown');
    cy.getBySel('image-list-input-page-number').as('page-num');
    cy.getBySel('image-list-btn-next-page').as('next-page');
    cy.getBySel('image-list-btn-prev-page').as('prev-page');
    cy.getBySel('image-list-select-classification').as('classification');

    cy.get('@page-num').clear().type('0');
    cy.contains('GOTO PAGE').click();

    const num_per_page = 12;
    const currPage = Math.ceil(1000 / num_per_page) - 1;
    const maxPage = Math.ceil(9000 / num_per_page) - 1;

    cy.get('@page-num').should('have.value', 0);
    cy.get('@next-page').click();
    cy.get('@next-page').click();
    cy.get('@page-num').should('have.value', 2);
    cy.reload();
    cy.checkSessionStorageObj('image_page_history', 'validation', 2);

    cy.get('@classification').click({ force: true });
    cy.contains('Incorrectly Classified').click();

    // cy.getBySel('image-list-div-all-imgs').children().should('have.length', 0);

    cy.get('@page-num').clear().type('9999');
    cy.contains('GOTO PAGE').click();

    cy.get('@next-page').should('be.disabled');

    cy.get('@classification').click({ force: true });
    cy.contains('Correctly Classified').click();

    // cy.getBySel('image-list-div-all-imgs').children().should('have.length', 0);
    cy.get('@page-num').should('have.value', 0);
  });
});
