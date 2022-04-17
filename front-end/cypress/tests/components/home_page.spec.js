const TRAIN_PAGE = 'Train';
const TRAIN_PAGE_LINK = 'train-pad';
const INFLUENCE_PAGE = 'Influence';
const INFLUENCE_PAGE_LINK = 'influence-pad';
const PREDICT_PAGE = 'Predict';
const PREDICT_PAGE_LINK = 'image-list/train';
const ANNOTATE_PAGE = 'Annotate';
const ANNOTATE_PAGE_LINK = 'image-list/train';

describe('The Home Page', () => {
  beforeEach(() => {
    cy.visit('');
  });

  it('can navigate to training page', () => {
    cy.getBySel(`home-${TRAIN_PAGE}-entrance`).click();
    cy.url().should('have.string', TRAIN_PAGE_LINK);
  });

  it('can navigate to influence page', () => {
    cy.getBySel(`home-${INFLUENCE_PAGE}-entrance`).click();
    cy.url().should('have.string', INFLUENCE_PAGE_LINK);
  });

  it('can navigate to predict page', () => {
    cy.getBySel(`home-${PREDICT_PAGE}-entrance`).click();
    cy.url().should('have.string', PREDICT_PAGE_LINK);
  });

  it('can navigate to annotate page', () => {
    cy.getBySel(`home-${ANNOTATE_PAGE}-entrance`).click();
    cy.url().should('have.string', ANNOTATE_PAGE_LINK);
  });
});
