from expects import expect, equal
from mamba import description, it
from src.utils import should_update_mx_phone_number


with description(should_update_mx_phone_number) as self:

    with it('no matching result'):
        result = should_update_mx_phone_number('5510300000')
        expect(result).to(equal(False))

    with it('matching result with +52'):
        result = should_update_mx_phone_number('+525510300000')
        expect(result).to(equal(True))

    with it('matching result with +521'):
        result = should_update_mx_phone_number('+5215510300000')
        expect(result).to(equal(True))
