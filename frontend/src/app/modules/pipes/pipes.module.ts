import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BooleanPipe } from '../../pipes/boolean/boolean.pipe';

@NgModule({
    declarations: [BooleanPipe],
    imports: [
        CommonModule
    ],
    exports: [BooleanPipe]
})
export class PipesModule { }