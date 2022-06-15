describe('My First Passing Test', () => {
  it('Does not do much!', () => {
    expect(true).to.equal(true);
  });
});

describe('My First Failing Test', () => {
  it('Does not do much!', () => {
    expect(true).to.equal(false);
  });
});

describe('My First Visiting Test', () => {
  it('Visits the Kitchen Sink', () => {
    cy.visit('https://example.cypress.io');
    cy.contains('type').click();
    // Should be on a new URL which includes '/commands/actions'
    cy.url().should('include', '/commands/actions');
  });
});

describe('Hooks', () => {
  before(() => {
    // runs once before all tests in the block
  });

  beforeEach(() => {
    // runs before each test in the block
  });

  afterEach(() => {
    // runs after each test in the block
  });

  after(() => {
    // runs once after all tests in the block
  });
});
