describe('The Home Page', () => {
  beforeEach(() => {
    cy.visit('');
  });

  it('displays welcome message', () => {
    cy.get('h1').should('have.text', 'Welcome Home!');
  });
});
