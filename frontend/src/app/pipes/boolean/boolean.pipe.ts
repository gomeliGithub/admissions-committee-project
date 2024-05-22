import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
    name: 'boolean'
})
export class BooleanPipe implements PipeTransform {
    constructor () { }
    
    transform (value: number): string {
        return Boolean(value) === true ? "Да" : "Нет";
    }
}