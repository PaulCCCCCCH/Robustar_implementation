describe('The Config Page', () => {
  beforeEach(() => {
    cy.visit('config');
  });

  it('displays table of configs', () => {
    const configs = [
      'batch_size',
      'device',
      'image_padding',
      'image_size',
      'model_arch',
      'num_classes',
      'num_workers',
      'pre_trained',
      'shuffle',
      'weight_to_load',
    ];

    cy.get('.key').each(($el, index, $list) => {
      cy.wrap($el).should('contain', configs[index]);
    });
  });
});
