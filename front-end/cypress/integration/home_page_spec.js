describe('The Home Page', () => {
  beforeEach(() => {
    cy.visit('');
  });

  it('displays welcome message', () => {
    cy.get('h1').should('have.text', 'Welcome Home!');
    cy.contains('Auto Annotate').click();
    cy.url().should('eq', 'http://localhost:8080/#/auto-annotate');
  });
});
