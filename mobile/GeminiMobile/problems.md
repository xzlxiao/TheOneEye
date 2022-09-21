- [x] IonIcons的图标无法显示
> 需要修改gradle，[网址](https://github.com/oblador/react-native-vector-icons)

- [ ] ViewPropTypes has been removed from React Native. Migrate to ViewPropTypes exported from 'deprecated-react-native-prop-types'. 
> 由于react native 升级到 0.69.2导致，同时，难以降级到0.67
> 解决方案如下：
>> Nice discussion going on here, inspired me to implement a workaround in our app using patch-package.
1. Install patch-package into your project, as per the instructions.
2. Install deprecated-react-native-prop-types by running npm install deprecated-react-native-prop-types or yarn add deprecated-react-native-prop-types.
3. The invariant seems to be enforced in node_modules/react-native/index.js, starting at line 436:
![](https://user-images.githubusercontent.com/26887502/180035338-d1a0644a-f3bd-4485-a3da-dc5f340da86b.png)
>> So, change these lines to return the corresponding Prop Types from deprecated-react-native-prop-types instead:
![](https://user-images.githubusercontent.com/26887502/180035916-16b5be9b-c9c1-406d-b46e-e2e93bda5cf9.png)
4. Save and run npx patch-package react-native to save the patch.
5. Rebuild and the app should launch.
>> Only thing to keep in mind is that this patch will need to be reapplied with every upgrade to react-native, or until the libraries in question are updated to import from deprecated-react-native-prop-types instead.