describe('ImageList', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8080/#/image-list/train');
  });

  it('Goes to the page for the target', () => {
    cy.contains('Class Name').click({ force: true });
    cy.contains('cat').click();
    cy.contains('GOTO CLASS').click();

    // It is WRONG to do the following! Value in pageNumDOM will not be refreshed properly!
    // Instead, use .as to create alias
    /*
        const pageNumDOM = cy.getBySel('image-list-input-page-number');
        pageNumDOM.should('include', 125);
        // do some other stuff
        pageNumDOM.should('include', 127);
     */

    cy.getBySel('image-list-input-page-number').as('page-num').should('have.value', 125);
    cy.getBySel('image-list-btn-next-page').as('next-page').click();
    cy.get('@next-page').click();
    cy.get('@page-num').should('have.value', 127);

    cy.getBySel('image-list-img-1').trigger('mouseenter'); // 'mouseover' does not trigger the overlay!
    cy.getBySel('image-list-btn-edit-image-1').click();
  });
});
